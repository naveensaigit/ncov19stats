from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import column,layout
from bokeh.models import HoverTool,ColumnDataSource,CustomJS
from bokeh.models.widgets import DateRangeSlider
# from bokeh.models.ranges import FactorRange
import numpy as np
from datetime import date,datetime,timedelta

def nptodt(dt):
     return datetime.strftime(datetime.strptime(str(dt),'%Y-%m-%d').date(),'%b-%d')

output_file('bokehtrial.html')
N=50
stdate=np.datetime64('2020-01-30')
enddate=np.datetime64((datetime.utcnow()+timedelta(hours=5,minutes=30)).date())
N=int((enddate-stdate)/np.timedelta64(1,'D'))
x=[str(x) for x in range(1,N+1)]
dates=[nptodt(x) for x in np.arange(stdate,stdate+N)]
stdate=date(2020,1,30)
enddate=(datetime.utcnow()+timedelta(hours=5,minutes=30)-timedelta(days=1)).date()

# Confirmed
newconf=np.array([np.random.randint(N) for i in range(N)])
cumconf=np.zeros(N)
cumconf[0]=newconf[0]
for i in range(1,N):
    cumconf[i]=newconf[i]+cumconf[i-1]
oldconf=list(cumconf-newconf)
cumconf=list(cumconf)
newconf=list(newconf)

#Active
newact=np.array([np.random.randint(N) for i in range(N)])
cumact=np.zeros(N)
cumact[0]=newact[0]
for i in range(1,N):
    cumact[i]=newact[i]+cumact[i-1]
cumact=list(cumact)

#Recovered
newrec=np.array([np.random.randint(N) for i in range(N)])
cumrec=np.zeros(N)
cumrec[0]=newrec[0]
for i in range(1,N):
    cumrec[i]=newrec[i]+cumrec[i-1]
oldrec=list(cumrec-newrec)
cumrec=list(cumrec)
newrec=list(newrec)

#Deceased
newdec=np.array([np.random.randint(N) for i in range(N)])
cumdec=np.zeros(N)
cumdec[0]=newdec[0]
for i in range(1,N):
    cumdec[i]=newdec[i]+cumdec[i-1]
olddec=list(cumdec-newdec)
cumdec=list(cumdec)
newdec=list(newdec)

data={'x':x,'dates':dates,'dispdates':dates,'oldconf':oldconf,'dispoldconf':oldconf,
      'newconf':newconf,'dispnewconf':newconf,'cumconf':cumconf,'dispcumconf':cumconf}

source = ColumnDataSource(data=data)

fig=figure(x_range=x,plot_height=300,title='Confirmed',background_fill_color=(255, 123, 0,0.15),
           toolbar_location='below'
           ,tools="wheel_zoom,box_zoom,reset, save")

callback=CustomJS(args=dict(source=source,x_range=fig.x_range),code='''
var stdate= new Date(2020,0,30);
var d1=(cb_obj.value[0]-stdate)/86400000;
var d2=(cb_obj.value[1]-stdate)/86400000;
x_range.setv({"start":0,"end":d2-d1+1});
d1=Math.floor(d1);
d2=Math.floor(d2);
source.data['dispoldconf']=source.data["oldconf"].slice(d1,d2+1);
source.data['dispnewconf']=source.data["newconf"].slice(d1,d2+1);
source.data['dispcumconf']=source.data["cumconf"].slice(d1,d2+1);
source.data['dispdates']=source.data["dates"].slice(d1,d2+1);
source.change.emit();
''')

fig.vbar_stack(['dispoldconf','dispnewconf'],x='x',width=0.4,
               color=[(255, 123, 0,0.5),(255, 123, 0,1)],
               source=source)

fig.add_tools(HoverTool(tooltips=[("Date","@dispdates"),("Old","@dispoldconf"),("New", "@dispnewconf"),
                                   ("Total", "@dispcumconf")]))

slider = DateRangeSlider(width=300,title="Date",callback_policy='mouseup',tooltips=False,start=stdate, end=enddate, value=(stdate,enddate), step=1)
slider.js_on_change('value', callback)
l = layout(children=[[slider]])

fig.y_range.start = 0
fig.xgrid.grid_line_color = None
fig.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
fig.xaxis.minor_tick_line_color = None
fig.xaxis.major_label_text_font_size = '0pt'
fig.xgrid.grid_line_color = None
fig.ygrid.grid_line_color = None

data1={'x':x,'dates':dates,'dispdates':dates,'cumact':cumact,'dispcumact':cumact}

source1 = ColumnDataSource(data=data1)

fig1=figure(x_range=x,plot_height=300,title='Active',background_fill_color=(255,0,0,0.15),
           toolbar_location='below'
           ,tools="wheel_zoom,box_zoom,reset, save")

callback1=CustomJS(args=dict(source=source1,x_range=fig1.x_range),code='''
var stdate= new Date(2020,0,30);
var d1=(cb_obj.value[0]-stdate)/86400000;
var d2=(cb_obj.value[1]-stdate)/86400000;
x_range.setv({"start":0,"end":d2-d1+1});
d1=Math.floor(d1);
d2=Math.floor(d2);
source.data['dispcumact']=source.data["cumact"].slice(d1,d2+1);
source.data['dispdates']=source.data["dates"].slice(d1,d2+1);
source.change.emit();
''')
fig1.vbar(x='x',top='dispcumact',width=0.4,source=source1,fill_color=(255,0,0),
          line_color=(255,0,0))

fig1.add_tools(HoverTool(tooltips=[("Date","@dispdates"),("Total", "@dispcumact")]))

slider1 = DateRangeSlider(width=300,title="Date",callback_policy='mouseup',tooltips=False,start=stdate, end=enddate, value=(stdate,enddate), step=1)
slider1.js_on_change('value', callback1)
l1 = layout(children=[[slider1]])

fig1.y_range.start = 0
fig1.xgrid.grid_line_color = None
fig1.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
fig1.xaxis.minor_tick_line_color = None
fig1.xaxis.major_label_text_font_size = '0pt'
fig1.xgrid.grid_line_color = None
fig1.ygrid.grid_line_color = None

data2={'x':x,'dates':dates,'dispdates':dates,'oldrec':oldrec,'dispoldrec':oldrec,
      'newrec':newrec,'dispnewrec':newrec,'cumrec':cumrec,'dispcumrec':cumrec}

source2 = ColumnDataSource(data=data2)

fig2=figure(x_range=x,plot_height=300,title='Recovered',background_fill_color=(0,255,100,0.15),
           toolbar_location='below'
           ,tools="wheel_zoom,box_zoom,reset, save")

callback2=CustomJS(args=dict(source=source2,x_range=fig2.x_range),code='''
var stdate= new Date(2020,0,30);
var d1=(cb_obj.value[0]-stdate)/86400000;
var d2=(cb_obj.value[1]-stdate)/86400000;
x_range.setv({"start":0,"end":d2-d1+1});
d1=Math.floor(d1);
d2=Math.floor(d2);
source.data['dispoldrec']=source.data["oldrec"].slice(d1,d2+1);
source.data['dispnewrec']=source.data["newrec"].slice(d1,d2+1);
source.data['dispcumrec']=source.data["cumrec"].slice(d1,d2+1);
source.data['dispdates']=source.data["dates"].slice(d1,d2+1);
source.change.emit();
''')

fig2.vbar_stack(['dispoldrec','dispnewrec'],x='x',width=0.4,
               color=[(50,205,50,0.5),(50,205,50,1)],
               source=source2)

fig2.add_tools(HoverTool(tooltips=[("Date","@dispdates"),("Old","@dispoldrec"),
                                   ("New", "@dispnewrec"),("Total", "@dispcumrec")]))

slider2 = DateRangeSlider(width=300,title="Date",callback_policy='mouseup',tooltips=False,start=stdate, end=enddate, value=(stdate,enddate), step=1)
slider2.js_on_change('value', callback2)
l2 = layout(children=[[slider2]])

fig2.y_range.start = 0
fig2.xgrid.grid_line_color = None
fig2.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
fig2.xaxis.minor_tick_line_color = None
fig2.xaxis.major_label_text_font_size = '0pt'
fig2.xgrid.grid_line_color = None
fig2.ygrid.grid_line_color = None

data3={'x':x,'dates':dates,'dispdates':dates,'olddec':olddec,'dispolddec':olddec,
      'newdec':newdec,'dispnewdec':newdec,'cumdec':cumdec,'dispcumdec':cumdec}

source3 = ColumnDataSource(data=data3)

fig3=figure(x_range=x,plot_height=300,title='Deceased',background_fill_color=(77, 75, 75,0.15),
           toolbar_location='below'
           ,tools="wheel_zoom,box_zoom,reset, save")

callback3=CustomJS(args=dict(source=source3,x_range=fig3.x_range),code='''
var stdate= new Date(2020,0,30);
var d1=(cb_obj.value[0]-stdate)/86400000;
var d2=(cb_obj.value[1]-stdate)/86400000;
x_range.setv({"start":0,"end":d2-d1+1});
d1=Math.floor(d1);
d2=Math.floor(d2);
source.data['dispolddec']=source.data["olddec"].slice(d1,d2+1);
source.data['dispnewdec']=source.data["newdec"].slice(d1,d2+1);
source.data['dispcumdec']=source.data["cumdec"].slice(d1,d2+1);
source.data['dispdates']=source.data["dates"].slice(d1,d2+1);
source.change.emit();
''')

fig3.vbar_stack(['dispolddec','dispnewdec'],x='x',width=0.4,
               color=[(77, 75, 75,0.5),(77, 75, 75,1)],
               source=source3)

fig3.add_tools(HoverTool(tooltips=[("Date","@dispdates"),("Old","@dispolddec"),
                                   ("New", "@dispnewdec"),("Total", "@dispcumdec")]))

slider3 = DateRangeSlider(width=300,title="Date",callback_policy='mouseup',tooltips=False,start=stdate, end=enddate, value=(stdate,enddate), step=1)
slider3.js_on_change('value', callback3)
l3 = layout(children=[[slider3]])

fig3.y_range.start = 0
fig3.xgrid.grid_line_color = None
fig3.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
fig3.xaxis.minor_tick_line_color = None
fig3.xaxis.major_label_text_font_size = '0pt'
fig3.xgrid.grid_line_color = None
fig3.ygrid.grid_line_color = None


show(column(fig,l,fig1,l1,fig2,l2,fig3,l3,sizing_mode="stretch_width"))
