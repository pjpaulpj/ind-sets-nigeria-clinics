#----------------------------------------------------#
#--------Finding independent sets algorithm----------#
#--------Akshat Goel---------------------------------#
#--------IDinsight-----------------------------------#
#--------June 8th, 2017------------------------------#
#----------------------------------------------------#
'''
This code will take in a data-set in long-form and given an edge rule, convert it into 
a NetworkX graph object. 

The default edge rule is: two nodes are connected if they are more than 20 km apart.

This object can then be used to run graph algorithms.

In particular, this script runs the NetworkX clique removal algorithm to return 
maximal cliques found.

It then takes the largest clique found and exports it to an Excel sheet.

Timer output: 1 loop, best of 3: 6.74 s per loop

Here is information about my computer:
Model: 2011 MacBook Pro, Processor: 2.5 GHz Intel Core i5, Memory: 10 GB 1600 MHz DDR3

The run-time of clique removal and generally all these algorithms is O(V/((ln(V))^2)), 
with V being the number of nodes - from the NetworkX website.

With a complete data-set of 3000 nodes, the run-time of clique removal should be approximately
36 seconds to a minute (being conservative) in the worst case on a comparable computer. 

I haven't taken into account the time it takes to clean and pre-process the data.

Here's the procedure I used to make this calculation. I'm including it here because I 
don't have much experience with running time calculations, so if you do, please do check:

If f(V) is the running time of clique removal on a graph with V nodes, 
and the worst case running time is O(V/((ln(V))^2)), this means that 
f(V) <= C * (V/((ln(V))^2) where C is a constant.

Now we have two cases: 

Case 1: f(226)
Case 2: f(3000) - Assuming you have a complete data-set of 3000, works the same way for 
anything else. 

We do: 

f(3000)/f(226) to get a ratio of the time it would take. The constant cancels.
We multiply the time taken to run the script (6.74 s) by this ratio to get an estimate of
the time it will take to do 3000 nodes, and that's what gives 36 seconds. 

'''


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

## Method calls
data1 = clean_data(data)											 ## Cleaning
adj_matrix = create_adj_matrix(data1)								 ## Creating adjacency matrix 
G = create_graph(adj_matrix)										 ## Creating graph
cliques = approximation.clique_removal(G)[1]						 ## Removing and listing cliques
biggest = max([len(cliques[x]) for x in range(len(cliques))])		 ## Storing cardinality of largest set
cliques = np.array([list(x) for x in cliques if len(x) == biggest])	 ## Storing biggest cliques
cliques = cliques[:][:]+ 1											 ## Adding 1 to get clinic number
cliques = DataFrame(np.char.mod('K'+ '%04d', cliques))				 ## Adding location identifier 'K'
filepath = wd + 'solutions.xlsx'								 	 ## Storing filepath
cliques.T.to_excel(filepath, index=False)							 ## Writing to Excel file


'''
My understanding is that you want big independent sets to sample from, not necessarily the maximum. If this is correct,
I would recommend just finding maximal independent sets (or maximal cliques depending on how you define edges), and just 
picking the biggest set you get from these, rather than trying directly to use the approximation algorithms 
from NetworkX. 

Other algorithms I tried:

1) Maximal independent set algorithm

The maximal independent set algorithm is equivalent to finding cliques in the complement graph.

2) Maximum indepedent set algorithm

The approximate maximum indepedent set algorithm kept returning a set of size 1. 
I couldn't find a way to control the approximation quality. I may be doing something wrong,
but I couldn't find any obvious mistakes. If you want to give this a try, just copy and paste
the code below. 

If there is a way to terminate this after a particular amount of time, that would work too, 
but I couldn't find it.

3) Maximum clique finding algorithm

The approx. max_clique finding algorithm took an incredibly long time to run (> 12 hours), and 
still didn't give me a solution. I couldn't find a way to control the approximation quality here either.

4) How to run

To run any of these, just copy and paste into the 'Method calls' section above. 

maximal_set = nx.maximal_independent_set(G) 			## Running maximal independent set algorithm from networkX
ap_max_set = approximation.maximum_independent_set(G)	## Running maximum independent set algorithm from networkX
ap_max_clique = approximation.max_clique(G)				## Running maximum clique finding algorithm from networkX.


5) Visualization 

I wrote this method to visualize the entire graph after creating it. There are 2 empty nodes in this sample.
As a basic sanity check, I wanted to see how these would show up.

I didn't have time to visualize the solution - we'll have to modify the show_graph method to do this. 

It will likely be more useful to visualize the solution directly in QGis anyway though, and not as a graph,
but let me know if I can help change anything in this code.

## Plotting graph

def show_graph(gr, title):
    
	# Given an NetworkX graph use NetworkX and matlpotlib to plot the graph
	nx.draw_networkx(gr, pos = nx.fruchterman_reingold_layout(gr), with_labels = False, node_size = 5, width = 0.3)
	plt.title(title)
	plt.show() 


## Graph method call:

show_graph(G,r'$\mathrm{Visualization\ of\ Clinic\ distances\ in\ km}$')  

'''












