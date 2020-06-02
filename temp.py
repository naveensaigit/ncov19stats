#To make changes to the database
from app import db
from datetime import date,timedelta,datetime
import pandas as pd
import urllib
import json
import numpy as np
from models import state

states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi','Dadra and Nagar Haveli and Daman and Diu','Goa', 'Gujarat',  'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',    'Kerala', 'Ladakh','Lakshadweep' , 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',    'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan','Sikkim',    'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal','State Unassigned','Total']
time_series={"time_series":{},"labels":[str(dt) for dt in np.arange(np.datetime64('2020-01-30'),np.datetime64('2020-03-14'))]}

for state in states:
    res=np.array(list(db.session.execute("select * from state where date<'2020-03-14' and statename='{}'".format(state))))
    time_series["time_series"].update({state:[list(res[:,i]) for i in range(2,9)]})

with urllib.request.urlopen("https://api.covid19india.org/data.json") as url:
        data = json.loads(url.read().decode())

state_codes={}

for row in data["statewise"]:
    state_codes.update({row["statecode"].lower():row["state"]})

time_series.update({"state_codes":state_codes})

with open('time_series.json','w') as f:
    json.dump(time_series,f)

with urllib.request.urlopen("https://raw.githubusercontent.com/naveensaigit/ReactApp/master/time_series.json") as url:
        test = json.loads(url.read().decode())