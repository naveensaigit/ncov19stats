from math import pi
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
from bokeh.layouts import column

output_file("pie.html")

status=['Active','Recovered','Deceased']
values=[100,32,10]
color=['#d11515','#1cb826','#4d4b4b']
angle=list(map(lambda x:x*2*pi/sum(values),values))
data={'status':status,'values':values,'color':color,'angle':angle}
source=ColumnDataSource(data=data)

p = figure(plot_height=330,plot_width=350, title="Cases Distribution", toolbar_location=None,
           tools="hover", tooltips="@status: @values", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.47,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='status', source=data)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None
show(p)