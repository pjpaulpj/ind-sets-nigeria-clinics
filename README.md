# ind-sets-clinics
This repository provides demo. Python code for finding the maximal cliques/independent sets of a graph. The data-set consists of geographical points. The goal is to find the largest set of points so that no two points are less than a given distance from each other. 

# Workflow

# graph-algorithm 
Here is the approximate workflow:  
1) Calculate the distance between any two points 
2) Define two points in the data to be connected if they are more than the given distance away from each other
3) Create an adjacency matrix representation of the graph 
4) Create a NetworkX graph object from this representation 
5) Save this object
6) Export this object to an AWS S3 bucket
7) Initate an AWS EC2 instance
8) Sync EC2 with S3 
9) Use approximate maximum clique algorithm from NetworkX  
8) Sync S3 with EC2 
9) Download .csv with results 

# circle-method
The repo. also contains two different versions of code which uses the following work-flow: 
1) Starts from a given initial point 
2) Draw a circle around this point of half the given distance 
3) Throw away anything within the circle 
4) Move to the nearest neighbour 
5) Repeat 

# contributions welcome! 
Here are tasks still remaining:  

# graph-algorithm 
1) Automate AWS execution using boto3 and cron 
2) Conduct solution checks
3) Re-organize solution checking files  

# circle-method 
1) Complete testing the pair-wise circle method file 
2) Get rid of the redundant distance() function in each file 


