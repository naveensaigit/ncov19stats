from flask import url_for,render_template,redirect,Flask,flash,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app=Flask(__name__,static_url_path='/public')
app.config['SECRET_KEY']='nlakengdpovhidgbarabgrk0x1'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://argdrfltcflwwn:81b4ca0e08de0376310bd4da065b38f68d3f09234fadcace5b8f7b0aa6c146b9@ec2-54-81-37-115.compute-1.amazonaws.com:5432/d54l0l0nemto94'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

def totals():
    res=db.session.execute("select * from state where statename='Total' and date='2020-04-26';").first()
    total={'Confirmed':[0,0],'Active':[0],'Recovered':[0,0],'Deceased':[0,0]}
    total['Confirmed'][1]+=res.dailyconf
    total['Recovered'][1]+=res.dailyrec
    total['Deceased'][1]+=res.dailydec
    total['Confirmed'][0]+=res.cumconf
    total['Active'][0]+=res.cumact
    total['Recovered'][0]+=res.cumrec
    total['Deceased'][0]+=res.cumdec
    return total
total=list(totals().items())

numbers=[['State/UT','Confirmed','Active','Recovered','Deceased']]
def statewise():
    res=db.session.execute("select * from state where date='{0}' order by cumconf desc".format(str(date(2020,4,26))))
    for i in res:
        numbers.append([i.statename,[i.cumconf,i.dailyconf],[i.cumact],[i.cumrec,i.dailyrec],[i.cumdec,i.dailyrec]])
    res=numbers[1]
    del numbers[1]
    numbers.append(res)
statewise()

colors=[['color:rgb(255, 123, 0)','background-color:rgba(255, 123, 0,0.2)'],['color:rgb(255, 0, 0)','background-color:rgba(255, 0, 0,0.2)'],
['color:rgb(0,255, 0)','background-color:rgba(0,255, 0,0.2)'],['color:rgb(77, 75, 75)','background-color:rgba(77, 75, 75,0.2)']]

@app.route('/')
def home():
    return render_template('index.html',numbers=numbers,total=total,colors=colors)

@app.route('/SIRD')
def sird():
    return render_template('sird.html',title='SIRD Model')

@app.route('/stats')
def stats():
    return 'stats'

if __name__=="__main__":
    app.run(debug=True)