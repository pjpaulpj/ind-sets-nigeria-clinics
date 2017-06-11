#----------------------------------------------------#
#--------Finding independent sets algorithm----------#
#--------Akshat Goel---------------------------------#
#--------IDinsight-----------------------------------#
#--------June 8th, 2017------------------------------#
#----------------------------------------------------#

## Importing packages
import numpy as np								## Numerical Python
import pandas as pd								## Pandas
import networkx as nx							## Networks
import matplotlib.mlab as mlab					## Graphing
import matplotlib.pyplot as plt 				## Graphing
import plotly as py								## Graphing
import plotly.graph_objs as go					## Graphing
from networkx.algorithms import approximation	## Approximation module is not automatically imported with NetworkX
from pandas import DataFrame					## Importing these to keep them on the namespace
from pandas import Series						## Importing these to keep them on the namespace	
from math import pi								## Going to use pi to calculate extent of data


## Setting working directory
wd = '/Users/Akshat/Desktop/mis/' 

## Storing the distance rule
radius = 10

## Loading data
data = pd.read_excel(wd + 'Katsina_sample_v1.xlsx')

## Data processing
def clean_data(data):
	
	## Copying the data
	data1 = data.copy()
	## Creating a boolean graph with variable 1 if two clinics are connected ( < radius km apart) and 0 otherwise
	data1['Distance (in kms)'] = (data1['Distance (in kms)'] > radius).astype(int)
	## Replacing own values to ensure that a node is not connected to itself
	mask = (data1.InputID == data1.TargetID)
	data1.loc[mask, 'Distance (in kms)'] = 0
	## Cleaning up memory
	del mask
	## Returning data with boolean values denoting edges as a Pandas data-frame
	return(data1) 

## Creating adjacency matrix representation of a graph
def create_adj_matrix(data):
	
	## Given a long form boolean edge list representation of a graph pivot data to create adjacency matrix
	adj_matrix = data.pivot(index='InputID', columns='TargetID', values='Distance (in kms)')
	return(adj_matrix)

## Constructing NetworkX graph from adjacency matrix representation input as a Pandas data-frame
def create_graph(adjacency_matrix):
    
    # Given an adjacency matrix use NetworkX to create a graph
    # Note that this function changes from indexing by clinic number to indexing by row and column indices
    # Python indexing begins with 0
	rows, cols = np.where(adjacency_matrix == 1)
	edges = zip(rows.tolist(), cols.tolist())
	gr = nx.Graph()
	gr.add_edges_from(edges)
	return(gr)

## Plotting graph

	

## Method calls
data1 = clean_data(data)											 ## Cleaning
adj_matrix = create_adj_matrix(data1)								 ## Creating adjacency matrix 
G = create_graph(adj_matrix)										 ## Creating graph
cliques = approximation.clique_removal(G)[1]						 ## Removing and listing cliques
biggest = max([len(cliques[x]) for x in range(len(cliques))])		 ## Storing cardinality of largest set
cliques = np.array([list(x) for x in cliques if len(x) == biggest])	 ## Storing biggest cliques
cliques = cliques[:][:]+ 1											 ## Adding 1 to get clinic number
cliques = DataFrame(np.char.mod('K'+ '%04d', cliques))				 ## Adding location identifier 'K'
filepath = wd + 'my_excel_file.xlsx'								 ## Storing filepath
cliques.T.to_excel(filepath, index=False)							 ## Writing to Excel file




'''



Other algorithms I tried:

1) Maximal indepedent set algorithm

The maximal independent set algorithm is equivalent to finding cliques in the complement graph.

2) Maximum indepedent set algorithm

The approximate maximum indepedent set algorithm kept returning a set of size 1. 
I couldn't find a way to control the approximation quality.

3) Maximum clique finding algorithm

The max_clique finding algorithm took an incredibly long time to run (> 12 hours), and 
still didn't give me a solution. I couldn't find a way to control the approximation quality here either.

4) How to run

To run any of these, just copy and paste into the 'method calls' section above. 

maximal_set = nx.maximal_independent_set(G) 			## Running maximal independent set algorithm from networkX
ap_max_set = approximation.maximum_independent_set(G)	## Running maximum independent set algorithm from networkX
ap_max_clique = approximation.max_clique(G)				## Running maximum clique finding algorithm from networkX.


5) Visualization 

I wrote this method to visualize the entire graph after creating it. There are 2 empty nodes in this sample.
As a basic sanity check, I wanted to see how these would show up.
I didn't have time to visualize the solution - this method will have to be modified. 
It will likely be more useful to visualize the solution directly in QGis anyway though, and not as a graph.

def show_graph(gr, title):
    
	# Given an NetworkX graph use NetworkX and matlpotlib to plot the graph
	nx.draw_networkx(gr, pos = nx.fruchterman_reingold_layout(gr), with_labels = False, node_size = 5, width = 0.3)
	plt.title(title)
	plt.show() 


Syntax for graph method call:

show_graph(G,r'$\mathrm{Visualization\ of\ Clinic\ distances\ in\ km}$')  

'''












