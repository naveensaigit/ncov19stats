import numpy as np
import pandas as pd
import shapefile as shp
import seaborn as sns

sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10,6))

sf = shp.Reader("india-polygon.shp")
sf.records()

#https://towardsdatascience.com/mapping-with-matplotlib-pandas-geopandas-and-basemap-in-python-d11b57ab5dac

def read_shapefile(sf):
    #fetching the headings from the shape file
    fields = [x[0] for x in sf.fields][1:]
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

df=read_shapefile(sf)

state_x=[]
state_y=[]

def plot_shape(id, s=None):
    # plt.figure()
    # #plotting the graphical axes where map ploting will be done
    # ax = plt.axes()
    # ax.set_aspect('equal')
    #storing the id number to be worked upon
    shape_ex = sf.shape(id)
    #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    x_lon = np.zeros((len(shape_ex.points)))
    #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    y_lat = np.zeros((len(shape_ex.points)))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    state_x.append(list(x_lon))
    state_y.append(list(y_lat))
    
    #plotting using the derived coordinated stored in array created by numpy
    # plt.plot(x_lon,y_lat) 
    # x0 = np.mean(x_lon)
    # y0 = np.mean(y_lat)
    #plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    #plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    #return x0, y0
    
for i in range(len(df)):
    plot_shape(i)

from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource,LinearColorMapper

    
palette=["#fff0f0", "#ffdbdb", "#ffd4d4", "#ff9696", "#ff6666", "#fa4848", "#ff3636", "#ff0000"]
palette1=["#ffe3bd","#ffd8a3","#ffc77a","#ffba5c","#ffaf42","#ffa933","#ffa121","#ff9300"]
palette2=["#d3ffcf","#a4ff9c","#7eff73","#70ff63","#59ff4a","#4bff3b","#3aff29","#14ff00"]
palette3=["#d2d4d2","#bbbdbb","#a4a6a4","#8d8f8d","#757875","#646664","#525452","#414241"]
cases=[np.random.randint(1000) for x in range(37)]
mapper=LinearColorMapper(palette=palette,low=0,high=max(cases))
colors= { 'field': cases, 'transform': mapper}
source=ColumnDataSource(dict(state_x=state_x,state_y=state_y,color=cases))

p = figure(title="", toolbar_location=None,
           plot_width=600, plot_height=750)

p.patches('state_x', 'state_y',source=source,
          fill_color={'field': 'color','transform': mapper}, 
          fill_alpha=0.7,
          line_color="white", line_width=0.5)

p.xaxis.major_tick_line_color = None  
p.xaxis.minor_tick_line_color = None  

p.yaxis.major_tick_line_color = None  
p.yaxis.minor_tick_line_color = None

p.xaxis.major_label_text_font_size = '0pt'  
p.yaxis.major_label_text_font_size = '0pt'

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

p.xaxis.visible = False
p.yaxis.visible = False
p.outline_line_color = None

output_file("choropleth.html", title="choropleth.py example")

show(column(p,sizing_mode='scale_width'))


# def plot_map(sf, x_lim = None, y_lim = None, figsize = (11,9)):
#     plt.figure(figsize = figsize)
#     id=0
#     for shape in sf.shapeRecords():
#         pts=list(shape.shape.points[:])
#         x = [i[0] for i in pts]
#         y = [i[1] for i in pts]
#         plt.scatter(x, y,s=1,c='black')
        
#         # if (x_lim == None) & (y_lim == None):
#         #     x0 = np.mean(x)
#         #     y0 = np.mean(y)
#         #     plt.text(x0, y0, id, fontsize=10)
#         # id = id+1
    
#     # if (x_lim != None) & (y_lim != None):     
#     #     plt.xlim(x_lim)
#     #     plt.ylim(y_lim)
#     mpld3.show()
# #calling the function and passing required parameters to plot the full map
# plot_map(sf)