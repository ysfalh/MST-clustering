from unionfind import *
from graph import Graph
import time

def KruskalMST(in_graph): 

	i = 0  
	e = 0 

	g = Graph(in_graph)

	start_time = time.time()

	g.graph = sorted(g.graph,key=lambda item: item[2]) 

	mst = {key : dict() for key in in_graph.keys()}
	parent = dict(); rank = dict()

	for vertice in g.vertices:
		parent[vertice]=vertice
		rank[vertice] = 0
	
	while e < g.V -1 : # we have to take V-1 edges

		u,v,w = g.graph[i]  
		i = i + 1
		x = find(parent, u) 
		y = find(parent, v) 


		if x != y: # if it doesn't cause cycle
			e = e + 1	
			mst[u][v] = mst[v][u] = w
			union(parent, rank, x, y)			  

	last = time.time() - start_time
	print("--- {0:.5f} seconds ---".format(last))
	
	return mst, last

