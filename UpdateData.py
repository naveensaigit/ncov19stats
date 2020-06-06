from app import db
from datetime import date,timedelta,datetime
import pandas as pd
import urllib
import json
import numpy as np
from models import state

def datechange(date):
    date=date.split('/')
    s=date[2]+'-'+date[1]+'-'+date[0]
    return np.datetime64(s)

states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi','Dadra and Nagar Haveli and Daman and Diu','Goa', 'Gujarat',  'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',    'Kerala', 'Ladakh','Lakshadweep' , 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',    'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan','Sikkim',    'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand','West Bengal','State Unassigned','Total']
stind=pd.Series(range(len(states)),states)
today=(datetime.utcnow()).date()

#Reading from API for today's new cases or update in last 2 days cases
with urllib.request.urlopen("https://api.covid19india.org/raw_data6.json") as url:
    data = json.loads(url.read().decode())

'''For testing
df=[]    
for row in data["raw_data"]:
    df.append(row.values())
df=pd.DataFrame(df,columns=data["raw_data"][0].keys())'''

ndays=1 #Update data for cases of last n days

for i in range(ndays,0,-1):
    db.session.execute("delete from state where date='{0}'".format(today-timedelta(days=i)))
db.session.commit()

for it in range(ndays,0,-1):
    time=[]
    for row in data['raw_data']:
        if row["dateannounced"]=="":
            continue
        dt=datetime.strptime(row["dateannounced"],'%d/%m/%Y').date()
        if row["detectedstate"]!='' and row["currentstatus"]!='' and row["numcases"]!='' and today-timedelta(days=it)==dt:
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

    res=db.session.execute("select * from state where date='{0}'".format(today-timedelta(days=it+1)))
    for i in res:
        ind=stind[i.statename]
        db.session.add(state(i.statename,today-timedelta(days=it),todaycases[ind][0],todaycases[ind][1],todaycases[ind][2],
        i.cumconf+todaycases[ind][0],i.cumact+todaycases[ind][0]-todaycases[ind][1]-todaycases[ind][2],i.cumrec+todaycases[ind][1],
        i.cumdec+todaycases[ind][2]))
    db.session.commit()