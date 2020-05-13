from flask import url_for,render_template,redirect,Flask,flash,request,session
from flask_sqlalchemy import SQLAlchemy
from sird import ret
from datetime import date,timedelta,datetime
import pandas as pd
import numpy as np
import urllib
import json

app=Flask(__name__,static_url_path='/public')
app.config['SECRET_KEY']='nlakengdpovhidgbarabgrk0x1'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://vznhvokezemmep:42d3129396b3c9755ca63f9ff2eed1c0ca0dc86a3e20a62164430e239cf18a96@ec2-3-216-129-140.compute-1.amazonaws.com:5432/d4lpe368cptbgn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

today=(datetime.utcnow()).date()
n=(np.datetime64(today)-np.datetime64('2020-01-30')-1)/np.timedelta64(1,'D')
end=1580342400000.0+n*86400000

db=SQLAlchemy(app)

#---------------------------------Queries-------------------------------------------------------

states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi','Dadra and Nagar Haveli and Daman and Diu','Goa', 'Gujarat',  'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',    'Kerala', 'Ladakh','Lakshadweep' , 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',    'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan','Sikkim',    'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',    'West Bengal','Total']
stind=pd.Series(range(len(states)),states)

def datechange(date):
    date=date.split('/')
    s=date[2]+'-'+date[1]+'-'+date[0]
    return np.datetime64(s)

def nptodt(dt):
     return datetime.strftime(datetime.strptime(str(dt),'%Y-%m-%d').date(),'%b-%d')

def read_today_api():
    #Reading from API for today's new cases
    with urllib.request.urlopen("https://api.covid19india.org/raw_data4.json") as url:
        data = json.loads(url.read().decode())

    #For testing
    #df=[]    
    #for row in data["raw_data"]:
    #    df.append(row.values())
    #df=pd.DataFrame(df,columns=data["raw_data"][0].keys())

    time=[]
    for row in data['raw_data']:
        if row["dateannounced"]=="":
            continue
        if row["detectedstate"]!='' and row["currentstatus"]!='' and row["numcases"]!='' and today==datetime.strptime(row["dateannounced"],'%d/%m/%Y').date():
            time.append([row["detectedstate"],datechange(row["dateannounced"]),row["currentstatus"],int(row["numcases"])])

    todaycases=[[0,0,0] for i in range(len(states))]

    for row in time:
        if row[2]=='Hospitalized':
            ind=0
        elif row[2]=='Recovered':
            ind=1
        else:
            ind=2
        todaycases[stind[row[0]]][ind]+=row[3]
        todaycases[36][ind]+=row[3]
    return todaycases

todaycases=read_today_api()

def totals(todaycases):
    res=db.session.execute("select * from state where statename='Total' and date='{0}';".format(str(today-timedelta(days=1)))).first()
    total={'Confirmed':[0,0],'Active':[0],'Recovered':[0,0],'Deceased':[0,0]}
    total['Confirmed'][1]+=todaycases[stind["Total"]][0]
    total['Recovered'][1]+=todaycases[stind["Total"]][1]
    total['Deceased'][1]+=todaycases[stind["Total"]][2]
    total['Confirmed'][0]+=(res.cumconf+todaycases[stind["Total"]][0])
    total['Recovered'][0]+=(res.cumrec+todaycases[stind["Total"]][1])
    total['Deceased'][0]+=(res.cumdec+todaycases[stind["Total"]][2])
    total['Active'][0]=total['Confirmed'][0]-total['Recovered'][0]-total['Deceased'][0]
    return total
total=list(totals(todaycases).items())

numbers=[['State/UT','Confirmed','Active','Recovered','Deceased']]
def statewise(todaycases):
    res=db.session.execute("select * from state where date='{0}' order by cumconf desc".format(str(today-timedelta(days=1))))
    for i in res:
        temp=todaycases[stind[i.statename]]
        numbers.append([i.statename,[i.cumconf+temp[0],temp[0]],[i.cumact+temp[0]-temp[1]-temp[2]],[i.cumrec+temp[1],temp[1]],[i.cumdec+temp[2],temp[2]]])
    res=numbers[1]
    del numbers[1]
    for i in range(1,len(numbers)):
        for j in range(1,len(numbers)):
            if numbers[i][1][0]>numbers[j][1][0]:
                temp=numbers[i]
                numbers[i]=numbers[j]
                numbers[j]=temp
    numbers.append(res)
statewise(todaycases)

def plotdata():
    plotdict={}
    for state in states:
        res=db.session.execute("select cumconf,cumact,cumrec,cumdec,cumconf-dailyconf as oldconf,cumrec-dailyrec as oldrec,cumdec-dailydec as olddec,dailyconf,dailyrec,dailydec,date from state where statename='{0}'".format(state)).fetchall()
        res=np.array(res)
        val=[]
        for i in range(res.shape[1]):
            if i==res.shape[1]-1:
                val.append(list(map(nptodt,res[:,i])))
            else:
                val.append(list(res[:,i]))
        val.append([str(x) for x in range(1,res.shape[0]+1)])
        plotdict.update({state:val})
    return plotdict
plotdict=plotdata()

plotsird=ret()
temp=np.array(plotdict['Total'])
plotsird.append(list(temp[0].astype(int)))
plotsird.append(list(temp[2].astype(int)))
plotsird.append(list(temp[3].astype(int)))
plotsird.append([nptodt(x) for x in np.arange(np.datetime64(today),np.datetime64(today)+10)])
plotsird.append(list(temp[0].astype(int)-temp[2].astype(int)-temp[3].astype(int)))
plotsird.append([nptodt(x) for x in np.arange(np.datetime64('2020-01-30'),np.datetime64(today))])
plotsird.append([1580342400000.0+x*86400000 for x in range(int(n+1))])


colors=[['color:rgb(255, 123, 0)','background-color:rgba(255, 123, 0,0.2)'],['color:rgb(255, 0, 0)','background-color:rgba(255, 0, 0,0.2)'],
['color:rgb(50,205,50)','background-color:rgba(50,205,50,0.2)'],['color:rgb(77, 75, 75)','background-color:rgba(77, 75, 75,0.2)']]

#---------------------------------Queries-------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html',numbers=numbers,total=total,plotdict=plotdict,states=states,colors=colors,end=end)

@app.route('/SIRD')
def sird():
    return render_template('sird.html',title='SIRD Model',plotsird=plotsird,n=int(n))

@app.route('/stats')
def stats():
    return render_template('stats.html',title='Statistics')

@app.route('/about')
def about():
    return render_template('about.html',title='About')

if __name__=="__main__":
    app.run(debug=True)