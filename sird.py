'''
Other parameters which fit a good model as well
beta, gamma, delta = 0.205, 1./11, 0.0055 dRdt=0.5*gamma*I

Prediction v 1.0
beta, gamma, delta = 0.2144, 1./20, 0.003
if t<=91:
                dSdt = -beta * math.exp(-t**1.05/200)* S * I / N
                dIdt = beta * math.exp(-t**1.05/200) *S * I / N - gamma * I - delta*I
        elif t>91 and t<=131:
            dSdt = -beta * math.exp(-t**1.1/200)* S * I / N
            dIdt = beta * math.exp(-t**1.1/200) *S * I / N - gamma * I - delta*I
        else:
            dSdt = -beta * math.exp(-t/350)* S * I / N
            dIdt = beta * math.exp(-t/350) *S * I / N - gamma * I - delta*I
        dRdt = 0.72*gamma*I
        dDdt = delta * I
'''
def ret():
    import urllib.request, json 
    with urllib.request.urlopen("https://api.covid19india.org/data.json") as url:
        data = json.loads(url.read().decode())
        
    data=data['cases_time_series']

    dataval=[]
    for row in data:
        dataval.append(list(row.values()))
    import pandas as pd
    df=pd.DataFrame(dataval,columns=list(data[0].keys()))
    DaysElapsed=len(df)
    import numpy as np
    from scipy.integrate import odeint
    import math
    import datetime
    if datetime.datetime.utcnow().date()!=datetime.datetime.now().date():
        DaysElapsed-=1

    # Total population, N.
    N = 1.3e9
    # Initial number of infected, recovered and dead individuals, I0, R0 and D0.
    I0, R0, D0 = 1, 0, 0
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0 -D0
    # Contact rate(beta), mean recovery rate(gamma) (in 1/days) and death rate(alpha)
    beta, gamma, delta = 0.2144, 1./20, 0.003
    #No. of days later (predicted)
    Days=450
    stdate=np.datetime64('2020-01-30')
    enddate=datetime.datetime.utcnow().date()
    t=np.arange(stdate,stdate+Days)
    # A grid of time points (in days)
    t1 = np.linspace(0, Days, Days)
    # The SIR model differential equations.
    def deriv(y, t, N, beta, gamma, delta):
        S, I, R, D = y
        if t<=91:
            dSdt = -beta * math.exp(-t**1.05/200)* S * I / N
            dIdt = beta * math.exp(-t**1.05/200) *S * I / N - gamma * I - delta*I
            dRdt = math.exp(-t**1.05/200)*gamma*I
        elif t>91 and t<=121:
            dSdt = -beta * math.exp(-t**1.09/200)* S * I / N
            dIdt = beta * math.exp(-t**1.09/200) *S * I / N - gamma * I - delta*I
            dRdt = math.exp(-t**0.8/200)*gamma*I
        else:
            dSdt = -beta * math.exp(-t**1.05/200)* S * I / N
            dIdt = beta * math.exp(-t**1.05/200) *S * I / N - gamma * I - delta*I
            dRdt = math.exp(-t**0.55/200)*gamma*I
        dDdt = 0.9*delta * I
        return dSdt, dIdt, dRdt, dDdt

    # Initial conditions vector
    y0 = S0, I0, R0, D0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t1, args=(N, beta, gamma, delta))
    S, I, R, D = ret.T
    I=I.astype(int)
    R=R.astype(int)
    D=D.astype(int)
    i=list(I)[:DaysElapsed]    
    r=list(R)[:DaysElapsed]
    d=list(D)[:DaysElapsed]
    return [i,r,d,I[DaysElapsed:DaysElapsed+10],R[DaysElapsed:DaysElapsed+10],D[DaysElapsed:DaysElapsed+10]]
'''
Code for plots

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.layouts import column
output_file("datetime.html")
dates=[nptodt(x) for x in np.arange(stdate,stdate+len(S))]
data={'x':t,'Sus':S, 'Inf':I, 'Rec': R, 'Dec':D,'dates':dates}
source=ColumnDataSource(data=data)
# create a new plot with a datetime axis type
fig = figure(plot_height=300, x_axis_type="datetime",
             tools="wheel_zoom,box_zoom,reset,save")

plt1=fig.line(x='x',y='Sus', color='orange', alpha=1,source=source)
fig.add_tools(HoverTool(renderers=[plt1],tooltips=[("Date","@dates"),("Susceptible", "@Sus")]))
plt2=fig.line(x='x',y='Inf', color='red', alpha=1,source=source)
fig.add_tools(HoverTool(renderers=[plt2],tooltips=[("Date","@dates"),("Infected", "@Inf")]))
plt3=fig.line(x='x',y='Rec', color='green', alpha=1,source=source)
fig.add_tools(HoverTool(renderers=[plt3],tooltips=[("Date","@dates"),("Recovered", "@Rec")]))
plt4=fig.line(x='x',y='Dec', color='gray', alpha=1,source=source)
fig.add_tools(HoverTool(renderers=[plt4],tooltips=[("Date","@dates"),("Deceased", "@Dec")]))

show(column(fig,sizing_mode="stretch_width"))

print(I[-1],R[-1],D[-1])

conf=np.array(df['totalconfirmed']).astype(np.float64)
rec=np.array(df['totalrecovered']).astype(np.float64)
dec=np.array(df['totaldeceased']).astype(np.float64)
act=conf-rec-dec

act=list(act)
conf=list(conf)
rec=list(rec)

dates=[nptodt(x) for x in np.arange(stdate,enddate)]
x=np.arange(stdate,enddate)

data={'x':x,'dates':dates,'actualact':act,'predact':I[:len(act)]}
source=ColumnDataSource(data=data)
# create a new plot with a datetime axis type
fig = figure(plot_height=300, x_axis_type="datetime",title='Active Cases',
             tools="wheel_zoom,box_zoom,reset,save")

plt1=fig.line(x='x',y='actualact', color='blue', alpha=1,source=source,legend_label='Actual')
fig.add_tools(HoverTool(renderers=[plt1],tooltips=[("Date","@dates"),("Actual", "@actualact")]))
plt2=fig.line(x='x',y='predact', color='orange', alpha=1,source=source,legend_label='Predicted')
fig.add_tools(HoverTool(renderers=[plt2],tooltips=[("Date","@dates"),("Predicted", "@predact")]))

fig.legend.location = "top_left"
fig.legend.click_policy="hide"
fig.xaxis.formatter=DatetimeTickFormatter(days=["%b %d"])

data1={'x':x,'dates':dates,'actualrec':rec,'predrec':R[:len(rec)]}
source1=ColumnDataSource(data=data1)
# create a new plot with a datetime axis type
fig1 = figure(plot_height=300, x_axis_type="datetime",title='Recovered Cases',
             tools="wheel_zoom,box_zoom,reset,save")

plt1=fig1.line(x='x',y='actualrec', color='blue', alpha=1,source=source1,legend_label='Actual')
fig1.add_tools(HoverTool(renderers=[plt1],tooltips=[("Date","@dates"),("Actual", "@actualrec")]))
plt2=fig1.line(x='x',y='predrec', color='orange', alpha=1,source=source1,legend_label='Predicted')
fig1.add_tools(HoverTool(renderers=[plt2],tooltips=[("Date","@dates"),("Predicted", "@predrec")]))

fig1.legend.location = "top_left"
fig1.legend.click_policy="hide"
fig1.xaxis.formatter=DatetimeTickFormatter(days=["%b %d"])

data2={'x':x,'dates':dates,'actualdec':dec,'preddec':D[:len(dec)]}
source2=ColumnDataSource(data=data2)
# create a new plot with a datetime axis type
fig2 = figure(plot_height=300, x_axis_type="datetime",title='Deceased Cases',
             tools="wheel_zoom,box_zoom,reset,save")

plt1=fig2.line(x='x',y='actualdec', color='blue', alpha=1,source=source2,legend_label='Actual')
fig2.add_tools(HoverTool(renderers=[plt1],tooltips=[("Date","@dates"),("Actual", "@actualdec")]))
plt2=fig2.line(x='x',y='preddec', color='orange', alpha=1,source=source2,legend_label='Predicted')
fig2.add_tools(HoverTool(renderers=[plt2],tooltips=[("Date","@dates"),("Predicted", "@preddec")]))

fig2.legend.location = "top_left"
fig2.legend.click_policy="hide"
fig2.xaxis.formatter=DatetimeTickFormatter(days=["%b %d"])

show(column(fig,fig1,fig2,sizing_mode="stretch_width"))

for i in range(1,11):
    print(act[DaysElapsed-i],I[DaysElapsed-i])
print()
for i in range(1,11):
    print(rec[DaysElapsed-i],R[DaysElapsed-i])
print()  
for i in range(1,11):
    print(dec[DaysElapsed-i],D[DaysElapsed-i])'''
