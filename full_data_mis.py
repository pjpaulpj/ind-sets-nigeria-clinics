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
import networkx as nx
from networkx.algorithms import approximation
from pandas import DataFrame
from pandas import Series
import geopy
from geopy.distance import vincenty
from shapely.geometry import Point				

## Setting working directory 
wd = '/Users/Akshat/Desktop/mis/'

def create_distance_matrix(data, radius):
	'''
Creating distance matrix using Vincenty distance formula.'''
	
	## Creating co-ordinates as a two-element tuple and adding it to the data-set
	data['coords'] = data[['properties/latitude', 'properties/longitude']].apply(tuple, axis=1)
	## Creating distance matrix in kilometers (this does too much work because dist. mat. is symmetric)
	distances = np.array([vincenty(x,y).km for x in data['coords'] for y in data['coords']])
	## Reshaping data
	square = distances.reshape(len(data),len(data))
	## Indexing using pandas
	square = DataFrame(square, index = data.id, columns = data.id)
	### Return statement
	return(square)

## Creates adjacency matrix
def create_adj_matrix(data, distances, radius):	
''' 
Creating adjacency matrix representation of a graph 
given an edge-list representation as a pandas data-frame. '''
	
	## Creating adjacency matrix 
	adj_matrix = DataFrame(np.where(distances > radius, 1,0), index = data.id, columns = data.id)
	return(adj_matrix)

## Creates NetworkX graph from adjacency matrix
def create_graph(adjacency_matrix):
''' 
This function takes an adjacency matrix and uses NetworkX to create a graph.
Note that this function changes from indexing by clinic number to indexing by row and column indices.
Python indexing begins with 0. '''
    
	rows, cols = np.where(adjacency_matrix == 1)
	edges = zip(rows.tolist(), cols.tolist())
	gr = nx.Graph()
	gr.add_edges_from(edges)
	return(gr)
	
## Implement code
def deploy_graph(data = "health facilties ehealth africa.csv", rad = 20):
'''
This function deploys the code above on our data-set. It works as follows:
1) Loads the data
2) Creates adjacency matrix using the data
3) Transforms the adjacency matrix into a NetworkX object
4) Calls the pickle package to compress this object for upload to AWS S3. '''
	
	df=pd.read_csv(wd + data)
	dist = create_distance_matrix(data = data, radius = rad)
	adj_matrix = create_adj_matrix(data = df, radius = rad)
	graph = create_graph(adj_matrix)
	nx.write_gpickle(graph, wd + "test_" + str(rad) + ".gpickle")
	
## Method calls
deploy_graph()


'''
This code is run on an Amazon EC2 instance.

## Storing cardinality of largest set
cliques = approximation.clique_removal(graph)[1]
## Storing biggest cliques
biggest = max([len(cliques[x]) for x in range(len(cliques))])
 ## Adding 1 to get clinic number		 
cliques = np.array([list(x) for x in cliques if len(x) == biggest])	
## Adding location identifier 'K' 
cliques = cliques[:][:]+ 1
## Storing filepath											
cliques = DataFrame(np.char.mod('K'+ '%04d', cliques))
## Writing to Excel file				 
filepath = wd + 'solutions.xlsx'
## Exporting								 	 
cliques.T.to_excel(filepath, index=False)							
'''








