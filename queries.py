from datetime import date
from app import db

numbers=['State/UT','Confirmed','Active','Recovered','Deceased']

def statewise():
    res=db.session.execute("select * from state where date='{0}' order by cumconf desc".format(str(date(2020,4,26))))
    for i in res:
        print(i.statename,i.cumconf)

statewise()