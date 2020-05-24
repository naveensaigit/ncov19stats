import numpy as np
import pandas as pd
from datetime import date,datetime,timedelta
import datetime

states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi','Dadra and Nagar Haveli and Daman and Diu','Goa', 'Gujarat',
 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
 'Kerala', 'Ladakh','Lakshadweep' , 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
 'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan','Sikkim',
 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
 'West Bengal','State Unassigned','Total']
stind=pd.Series(range(len(states)),states)

stdate=np.datetime64('2020-01-30')
enddate=np.datetime64((datetime.datetime.utcnow()+datetime.timedelta(hours=5,minutes=30)).date())
dates=np.arange(np.datetime64('2020-01-30'),enddate)

def datechange(date):
    date=date.split('/')
    s=date[2]+'-'+date[1]+'-'+date[0]
    return np.datetime64(s)

def cuml(x):
    x[0][3]=x[0][0]
    x[0][5]=x[0][1]
    x[0][6]=x[0][2]
    x[0][4]=x[0][3]-x[0][1]-x[0][2]
    for i in range(1,len(x)):
        x[i][3]+=(x[i-1][3]+x[i][0])
        x[i][5]+=(x[i-1][5]+x[i][1])
        x[i][6]+=(x[i-1][6]+x[i][2])
        x[i][4]=x[i][3]-x[i][5]-x[i][6]
    return x

import urllib.request, json 
with urllib.request.urlopen("https://api.covid19india.org/raw_data1.json") as url:
    data = json.loads(url.read().decode())
    
time=[]
needed=["dateannounced","detectedstate"]
for row in data['raw_data']:
    if row["detectedstate"]!='':
        time.append([row["detectedstate"],datechange(row["dateannounced"]),int(row["numcases"])])

with urllib.request.urlopen("https://api.covid19india.org/raw_data2.json") as url:
    data = json.loads(url.read().decode())
    
for row in data['raw_data']:
    if row["detectedstate"]!='':
        time.append([row["detectedstate"],datechange(row["dateannounced"]),int(row["numcases"])])
    
with urllib.request.urlopen("https://api.covid19india.org/deaths_recoveries.json") as url:
    data = json.loads(url.read().decode())

rec=[]
needed2=["date","state"]

for row in data["deaths_recoveries"]:
    if row["state"]!='':
        rec.append([row["state"],datechange(row["date"]),row["patientstatus"]])
        
timeseries=[]
for i in range(len(states)):
    timeseries.append([])
    for date in dates:
        timeseries[i].append([0,0,0,0,0,0,0])
                             
for row in time:
        timeseries[stind[row[0]]][int(str(row[1]-stdate).split()[0])][0]+=row[2]
        
for row in rec:
    if row[2]=='Recovered':
        timeseries[stind[row[0]]][int(str(row[1]-stdate).split()[0])][1]+=1
    elif row[2]=='Deceased':
        timeseries[stind[row[0]]][int(str(row[1]-stdate).split()[0])][2]+=1

with urllib.request.urlopen("https://api.covid19india.org/raw_data3.json") as url:
    data = json.loads(url.read().decode())
    
time=[]
for row in data['raw_data']:
    if row["detectedstate"]!='' and row["currentstatus"]!='' and row["numcases"]!='':
        time.append([row["detectedstate"],datechange(row["dateannounced"]),row["currentstatus"],int(row["numcases"])])
        
with urllib.request.urlopen("https://api.covid19india.org/raw_data4.json") as url:
    data = json.loads(url.read().decode())
    
for row in data['raw_data']:
    if row["detectedstate"]!='' and row["currentstatus"]!='' and row["numcases"]!='':
        time.append([row["detectedstate"],datechange(row["dateannounced"]),row["currentstatus"],int(row["numcases"])])

for row in time:
    if row[1]==enddate:
        continue
    if row[2]=='Hospitalized':
        ind=0
    elif row[2]=='Recovered':
        ind=1
    else:
        ind=2
    timeseries[stind[row[0]]][int(str(row[1]-stdate).split()[0])][ind]+=row[3]

    
for i in range(len(timeseries)):
    timeseries[i]=cuml(timeseries[i])
    
#For Nation-Wide cases, Total
for i in range(len(timeseries)-1):
    for j in range(len(timeseries[i])):
        for k in range(7):        
            timeseries[-1][j][k]+=timeseries[i][j][k]
            
from models import state
from app import db

for i in range(len(timeseries)):
    for j in range(len(dates)):
        db.session.add(state(statename=states[i],date= datetime.datetime.strptime(str(dates[j]),'%Y-%m-%d').date(),dailyconf=timeseries[i][j][0],dailyrec=timeseries[i][j][1], dailydec=timeseries[i][j][2],cumconf=timeseries[i][j][3],cumact=timeseries[i][j][4],cumrec=timeseries[i][j][5], cumdec=timeseries[i][j][6]))

db.session.commit()