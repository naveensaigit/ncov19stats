import urllib.request, json 
with urllib.request.urlopen("https://api.covid19india.org/data.json") as url:
    data = json.loads(url.read().decode())
    
data=data['cases_time_series']

dataval=[]
for row in data:
    dataval.append(list(row.values()))
import pandas as pd
df=pd.DataFrame(dataval,columns=list(data[0].keys()))
import numpy as np

arr=list(df['totalconfirmed'])
arr1=list(df['totalrecovered'])
arr2=list(df['totaldeceased'])

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

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.layouts import column
import datetime
output_file("double.html")

def nptodt(dt):
     return datetime.datetime.strftime(datetime.datetime.strptime(str(dt),'%Y-%m-%d').date(),'%d-%b-%Y')

stdate=np.datetime64('2020-01-30')
t=np.arange(stdate,stdate+len(cdb))
dates=[nptodt(x) for x in t ]
data={'x':list(t),'conf':list(cdb), 'rec':list(rdb), 'dec':list(ddb),'dates':list(dates)}
source=ColumnDataSource(data=data)
# create a new plot with a datetime axis type
fig = figure(plot_height=300, x_axis_type="datetime",
             tools="wheel_zoom,box_zoom,reset,save",title='Cases Doubling Rates')

plt1=fig.line(x='x',y='conf', color='orange', alpha=1,legend_label='Confirmed',source=source)
fig.add_tools(HoverTool(renderers=[plt1],tooltips=[("Date","@dates"),("Confirmed Rate", "@conf")]))
plt3=fig.line(x='x',y='rec', color='green', alpha=1,legend_label='Recovered',source=source)
fig.add_tools(HoverTool(renderers=[plt3],tooltips=[("Date","@dates"),("Recovered Rate", "@rec")]))
plt4=fig.line(x='x',y='dec', color='gray', alpha=1,legend_label='Deceased',source=source)
fig.add_tools(HoverTool(renderers=[plt4],tooltips=[("Date","@dates"),("Deceased Rate", "@dec")]))
fig.xaxis.formatter=DatetimeTickFormatter(days=["%b %d"])
fig.legend.location='top_lef'
fig.legend.click_policy='hide'
show(column(fig,sizing_mode="stretch_width"))

output_file("r0.html")
r0=[]
for i in cdb:
    if i:
        r0.append(1+11.5*0.693/i)
    else:
        r0.append(1+11.5*0.693)
        
data={'x':list(t),'r0':list(r0),'dates':list(dates)}
source=ColumnDataSource(data=data)
fig = figure(plot_height=300, x_axis_type="datetime",
             tools="wheel_zoom,box_zoom,reset,save",title='Basic Reproduction Number')

plt1=fig.line(x='x',y='r0', color='red', alpha=1,source=source)
fig.add_tools(HoverTool(renderers=[plt1],tooltips=[("Date","@dates"),("R0", "@r0")]))
show(column(fig,sizing_mode="stretch_width"))