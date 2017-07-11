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

## Importing packages
import numpy as np
import pandas as pd	
import random
import geopy


from geopy.distance import vincenty
from shapely.geometry import Point	

## Setting random seed
random.seed()			

## Setting working directory 
wd = '/Users/Akshat/Desktop/mis/'

def create_distance_matrix(data):
	'''
	Creating distance matrix using Vincenty distance formula.'''
	
	## Creating co-ordinates as a two-element tuple and adding it to the data-set
	data['coords'] = data[['properties/latitude', 'properties/longitude']].apply(tuple, axis=1)
	## Creating distance matrix in kilometers (this does too much work because dist. mat. is symmetric)
	distances = np.array([vincenty(x,y).km for x in data['coords'] for y in data['coords']])
	## Reshaping data
	square = distances.reshape(len(data),len(data))
	## Indexing using pandas
	square = pd.DataFrame(square, index = data.id, columns = data.id)
	### Return statement
	return(square)
	
def circle_draw(row, distances, radius):
	''' This function takes in a clinic name. 
		It takes in a set of clinic distances.
		It takes a radius. 
		It outputs the set of distances for clinics at least more than 'radius' distance away 
		from the current clinic. 
		It also outputs a set of neighbours for the current clinic so that 
		we can choose the next point.'''
	
	# Getting distance data for the current clinic
	data = distances[row]
	# Getting data for all those within radius1
	inside_circle = data[data < radius] 
	# Dropping columns within the circle
	distances = distances.drop(inside_circle.index, axis = 1)
	# Dropping rows within the circle
	distances = distances.drop(inside_circle.index)
	# Keep only those clinics which are further away than the given distance
	data = data[data >= radius]
	# Return statement
	return(distances, data)

def circle_method(distances, radius1, radius2, initial_clinic): 
	''' 
	This function takes in a distance matrix, and radius,
	and outputs a solution matrix by using the circle method.'''
	
	# Initializing running list of candidate solution
	dist1 = distances
	# Initializing solution list
	solution = []
	# Initializing counter
	is_even=0
	# Initializing starting point
	row = initial_clinic
	# Entering while loop
	while dist1.empty == False:
		# Updating counter 
		is_even += 1	
		# Dropping all clinics less than first radius away
		if is_even % 2 == 1:
			# Processing this point
			dist1, data = circle_draw(row, dist1, radius1)
			# Checking if neighbour set is empty
			if data.empty:
				continue 
			# Else making the pair
			else:
				# Pair construction
				pair = [row, data.idxmin()]
				# Pushing pair to solution list
				solution.append(pair)
				print(solution)
		else:
        	# Getting pair names
			point1, point2 = pair		
			# Updating distances for first point in pair
			dist2, data1 = circle_draw(point1, dist2, radius2)
			# Updating distances for second point in pair
			dist3, data2 = circle_draw(point2, dist2, radius2) 
			# Checking to see if there are no neighbours
			if data1.empty and data2.empty:
				continue 
			# Moving to the nearest neighbour
			elif data1.empty or data2.min() < data1.min():
				row = data2.idxmin()
			elif data2.empty or data1.min() < data2.min():
				row = data1.idxmin()					
	# Return solution
	return(solution)
		
def deploy_circle(data = "health facilties ehealth africa.csv", rad1 = 15, rad2 = 20):
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
	solution = circle_method(distances = dist, radius1 = rad1, radius2=rad2, initial_clinic = 'zamafara_katsina_hf.450')
	# Returning solution
	# Return statement
	return(dist, solution)
	
## Method calls
solution = deploy_circle()
print(len(solution[1]))
