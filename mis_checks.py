#----------------------------------------------------#
#--------Finding independent sets algorithm----------#
#--------Akshat Goel---------------------------------#
#--------IDinsight-----------------------------------#
#--------June 8th, 2017------------------------------#
''' 
This script will do a check to see whether
the maximal clique algorithm run on the 
New Incentives data is producing solutions.
For any questions related to this file, 
please contact Akshat Goel at akshat.goel@idinsight.org.
'''

## Importing packages
import numpy as np								
import pandas as pd								
import networkx as nx							
from networkx.algorithms import approximation	
import geopy, folium																					
from geopy.distance import vincenty				
from shapely.geometry import Point			
import re										


# Setting working directory
wd = '/Users/Akshat/Desktop/mis/'

# Loading data
df=pd.read_csv(wd + "health facilties ehealth africa.csv")

# Loading solutions
solution = pd.read_excel(wd + "solutions.xlsx")

# Stripping leading characters and converting to integer 
solution = solution[0].str.replace('K', '', case = False).astype(int)

# Subtracting by 1
solution = solution[:][:] - 1

# Getting solutions
solution1 = df.iloc[solution]

# Solution Excel sheet
solution1.to_excel(wd +'solutions10km.xlsx', index=False)

# Adding solution variable
df['sol'] = 0

# Marking solutions
df.iloc[solution, df.columns.get_loc('sol')] = 1

# Color function for map
def color(sol):
	''' Takes in an indicator for whether we are 
	at a solution or not and colors accordingly.'''   
    	
	# Color those points which are solutions
	if sol == 1:
		col='#ff0101'
	# Color those points which are not solutions 
	else:
		col='#000000'
	# Return statement
	return(col)

# This function creates an interactive map using Folium to visualize the solution to the maximal independent set problem
def create_map(df):

	# Creating map object
	map=folium.Map(location=[df['properties/latitude'].mean(),
				 df['properties/longitude'].mean()], 
		       zoom_start=6, tiles='Stamen Toner')
	# Creating feature locations object
	fg=folium.FeatureGroup(name="Clinic Locations")
	# This counts the number of iterations
	counter = 0
	# For loop to create markers
	for lat,lon,name,sol in zip(df['properties/latitude'],df['properties/longitude'],df['id'],df['sol']):
		# Creating map
		fg.add_child(folium.Marker(location=[lat,lon],
					   popup=(folium.Popup(name)), 
					   icon=folium.Icon(color=color(sol),
							    icon_color='green')))
		# Printing counter to keep track
		print(counter)
		# Updating counter
		counter +=1	
	
	# Adding to base layer
	map.add_child(fg)
	# Saving
	map.save(outfile='map.html')

# Method call	
create_map(df)									





















