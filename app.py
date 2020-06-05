from flask import url_for,render_template,redirect,Flask,flash,request,session
from flask_sqlalchemy import SQLAlchemy
from sird import ret
from datetime import date,timedelta,datetime
import pandas as pd
import numpy as np
import urllib
import json

app=Flask(__name__,static_url_path='/public')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY']='nlakengdpovhidgbarabgrk0x1'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://psiqaapsokmaab:d18b45eeb3ebcf39d1e22ccde3204567289d6148fcf3b505dcf6ac6ab2d2d8c9@ec2-3-208-50-226.compute-1.amazonaws.com:5432/dbq0sgnbev17e3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

today=(datetime.utcnow()).date()
#today-=timedelta(days=3)
n=(np.datetime64(today)-np.datetime64('2020-01-30')-1)/np.timedelta64(1,'D')
end=1580342400000.0+n*86400000

db=SQLAlchemy(app)

#---------------------------------Queries-------------------------------------------------------

states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi','Dadra and Nagar Haveli and Daman and Diu','Goa', 'Gujarat',  'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',    'Kerala', 'Ladakh','Lakshadweep' , 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',    'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan','Sikkim',    'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal','State Unassigned','Total']
stind=pd.Series(range(len(states)),states)

def datechange(date):
    date=date.split('/')
    s=date[2]+'-'+date[1]+'-'+date[0]
    return np.datetime64(s)

def nptodt(dt):
     return datetime.strftime(datetime.strptime(str(dt),'%Y-%m-%d').date(),'%b-%d')

def read_today_api():
    #Reading from API for today's new cases
    with urllib.request.urlopen("https://api.covid19india.org/raw_data5.json") as url:
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
        todaycases[-1][ind]+=row[3]
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
    #numbers.append(["State Unassigned",[814,0],[814],[0,0],[0,0]])
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
        if state!='State Unassigned':
            res=db.session.execute("select cumconf,cumact,cumrec,cumdec,cumconf-dailyconf as oldconf,cumrec-dailyrec as oldrec,cumdec-dailydec as olddec,dailyconf,dailyrec,dailydec,date from state where statename='{0}' order by date".format(state)).fetchall()
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
labels=[nptodt(x) for x in np.arange(np.datetime64('2020-01-30'),np.datetime64(today))]
plotsird.append(labels)
dtms=[1580342400000.0+x*86400000 for x in range(int(n+1))]
plotsird.append(dtms)

def stats():
    drate={}
    grate={}
    r0={}
    for state in states:
        if state!='State Unassigned':
            res=db.session.execute("select cumconf,cumrec,cumdec from state where statename='{0}'".format(state)).fetchall()
            res=np.array(res)
            arr=res[:,0]
            if(int(arr[-1])==0):
                continue
            arr1=res[:,1]
            arr2=res[:,2]
            cdb=np.zeros(len(arr),dtype=int)
            rdb=np.zeros(len(arr),dtype=int)
            ddb=np.zeros(len(arr),dtype=int)
            for i in range(len(arr)):
                for j in range(i):
                    if float(arr[j])>=float(arr[i])/2:
                        cdb[i]+=(i-j)
                        break
                for j in range(i):
                    if float(arr1[j])>=float(arr1[i])/2:
                        rdb[i]+=(i-j)
                        break
                for j in range(i):
                    if float(arr2[j])>=float(arr2[i])/2:
                        ddb[i]+=(i-j)
                        break
            temp=[]
            for i in cdb:
                if i:
                    temp.append(1+11.5*0.693/i)
                else:
                    temp.append(1)
            r0.update({state:temp})
            drate.update({state:[list(cdb),list(rdb),list(ddb)]})
            temp=[]

            gry=0
            grdby=0
            if(int(arr[-2])!=0 and int(arr[-1])!=0):
                gry=(arr[-1]-arr[-2])/arr[-2]
            if(int(arr[-3])!=0 and int(arr[-2]!=0)):
                grdby=(arr[-2]-arr[-3])/arr[-3]
            temp.append([gry,gry-grdby])

            gry=0
            grdby=0
            if(int(arr1[-2])!=0 and int(arr1[-1])!=0):
                gry=(arr1[-1]-arr1[-2])/arr1[-2]
            if(int(arr1[-3])!=0 and int(arr1[-2]!=0)):
                grdby=(arr1[-2]-arr1[-3])/arr1[-3]
            temp.append([gry,gry-grdby])

            gry=0
            grdby=0
            if(int(arr2[-2])!=0 and int(arr2[-1])!=0):
                gry=(arr2[-1]-arr2[-2])/arr2[-2]
            if(int(arr2[-3])!=0 and int(arr2[-2]!=0)):
                grdby=(arr2[-2]-arr2[-3])/arr2[-3]
            temp.append([gry,gry-grdby])
            grate.update({state:temp})
    return drate,grate,r0
drate,grate,r0=stats()

statdict={}
for i in range(1,len(numbers)):
    statdict.update({numbers[i][0]:numbers[i][1:]})

colors=[['color:rgb(255, 123, 0)','background-color:rgba(255, 123, 0,0.2)'],['color:rgb(255, 0, 0)','background-color:rgba(255, 0, 0,0.2)'],
['color:rgb(50,205,50)','background-color:rgba(50,205,50,0.2)'],['color:rgb(77, 75, 75)','background-color:rgba(77, 75, 75,0.2)']]

refresh=datetime.now()
#---------------------------------Queries-------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html',numbers=numbers,total=total,plotdict=plotdict,states=states,colors=colors,end=end,refresh=refresh)

@app.route('/SIRD')
def sird():
    return render_template('sird.html',title='SIRD Model',plotsird=plotsird,n=int(n))

@app.route('/stats')
def stats():
    return render_template('stats.html',title='Statistics',total=statdict,colors=colors,drate=drate,grate=grate,r0=r0,labels=labels,dtms=dtms)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

if __name__=="__main__":
    app.run(debug=True)