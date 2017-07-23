## Importing packages
import numpy as np						## Numerical Python
import pandas as pd						## Pandas
import networkx as nx						## Networks
import matplotlib.mlab as mlab					## Graphing
import matplotlib.pyplot as plt 				## Graphing
import plotly as py						## Graphing
import plotly.graph_objs as go					## Graphing
from networkx.algorithms import approximation			## Approximation module is not automatically imported with NetworkX
from pandas import DataFrame					## Importing these to keep them on the namespace
from pandas import Series					## Importing these to keep them on the namespace	
import geopy, folium, geopandas					## Spatial analysis packages												
from geopy.distance import vincenty				## Importing distance calculator into namespace 
from geopandas import GeoSeries					## Importing geo.series constructor into namespace
from shapely.geometry import Point				## Importing point



## This function creates an interactive map using Folium to visualize the solution to the maximal independent set problem
def create_map(df):

	## Adding place-holder for solution initialized as a random variable from a standard normal
	df['sol'] = Series(np.random.randn(len(df['id'])), index=df.index)

	## Creating map object
	map=folium.Map(location=[df['properties/latitude'].mean(),df['properties/longitude'].mean()],zoom_start=6, tiles=''Stamen Toner')
	
	## Creating feature locations object
	fg=folium.FeatureGroup(name="Clinic Locations")
	
	## This counts the number of iterations
	counter = 0
	## For loop to create markers
	for lat,lon,name,sol in zip(df['properties/latitude'],df['properties/longitude'],df['properties/primary_name'],df['sol']):
		print(i)
		fg.add_child(folium.RegularPolygonMarker(location=[lat,lon],popup=(folium.Popup(name)), number_of_sides=2, radius=1))
		counter = i +1	
	## Adding
	map.add_child(fg)									

## Saving the map
outfp = wd + "base_map.html"
map.save(outfp)
