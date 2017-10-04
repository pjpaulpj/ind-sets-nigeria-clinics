#---------------------------------------------------------------------#
#--------Mapping and distance calculation for NI Clinics -------------#
#--------Akshat Goel--------------------------------------------------#
#--------IDinsight----------------------------------------------------#
#--------June 8th, 2017-----------------------------------------------#
#---------------------------------------------------------------------#
'''
This script calculates distances between clinics in the New Incentives
project data-set. It also computes a sampling frame. 

For any questions related to this file, please contact 
Akshat Goel at akshat.goel@idinsight.org.'''

# Importing packages
import numpy as np
import pandas as pd	
import random
from pandas import DataFrame
from pandas import Series
import geopy
from geopy.distance import vincenty
from shapely.geometry import Point	


# Setting random seed
random.seed()			

# Setting working directory 
wd = '/Users/Akshat/Desktop/mis/'

def create_distance_matrix(data):
	'''
	Creating distance matrix using Vincenty distance formula.'''
	
	# Creating co-ordinates as a two-element tuple and adding it to the data-set
	data['coords'] = data[['properties/latitude', 'properties/longitude']].apply(tuple, axis=1)
	# Creating distance matrix in kilometers (this does too much work because dist. mat. is symmetric)
	distances = np.array([vincenty(x,y).km for x in data['coords'] for y in data['coords']])
	# Reshaping data
	square = distances.reshape(len(data),len(data))
	# Indexing using pandas
	square = DataFrame(square, index = data.id, columns = data.id)
	# Return statement
	return(square)

def circle_method(distances, radius, initial_clinic = 'zamafara_katsina_hf.450'): 
	''' 
	This function takes in a distance matrix, and radius,
	and outputs a solution matrix by using the circle method.'''
	
	# Initializing solution list
	solution = []
	# Choosing an initial clinic
	row = initial_clinic
	# Entering while loop
	while distances.empty == False:
		# Pushing row to solution list
		solution.append(row)
		# Getting neighbours for the current clinic
		data = distances[row]
		# Dropping all clinics less than x km away
		inside_circle = data[data < radius]
		# Dropping columns within the circle
		distances = distances.drop(inside_circle.index, axis = 1)
		# Dropping rows
		distances = distances.drop(inside_circle.index)
		# Moving to the nearest neighbor
		# Keep only those clinics which are further away than the given distance
		data = data[data >= radius]
		# Then pick the closest point or pick a random point from solution candidates
		if data.empty and distances.empty:	
			break 
		elif data.empty:
			row = random.sample(list(distances.index), 1)[0] 
		else:
			row = data.idxmin()
	# Return solution
	return(solution)
		
def deploy_circle(data = "health facilties ehealth africa.csv", rad = 17):
	'''This function deploys the circle method code. It works as follows: 
	1) Loads the data
	2) Creates distance matrix
	3) Implements circle method on distance matrix
	4) Return solution '''
	
	# Loading data
	df=pd.read_csv(wd + data)
	# Creating distance matrix
	dist = create_distance_matrix(data = df)
	# Calling circle method
	solution = circle_method(distances = dist, radius = rad)
	# Return statement
	return(dist, solution)
	
# Method calls
solution = deploy_circle()
print(len(solution[1]))
sol = pd.DataFrame(solution[1])

# Writing output
filepath = wd + 'solutions17.xlsx' 
sol.to_excel(filepath, index = False) 
