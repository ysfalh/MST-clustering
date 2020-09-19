from unionfind import *
from graph import Graph
import time


def boruvska(in_graph): 
	parent = []; rank = []; 
	g = Graph(in_graph)
	mst = {key:{} for key in in_graph}

	# An array to store index of the cheapest edge of component
	cheapest =[] 

	# Initially there are V different trees (components)
	numTrees = g.V 
	MSTweight = 0

	# Create V subsets with single elements 
	for node in range(g.V): 
		parent.append(node) 
		rank.append(0) 
		cheapest =[-1] * g.V 

	# Keep combining components (or sets) until all 
	# components are not combined into single MST 
	start_time = time.time()

	while numTrees > 1: 

		# Traverse through all edges and update 
		# cheapest of every component 
		for i in range(len(g.graph)): 

			# Find components (or sets) of two corners 
			# of current edge 
			u,v,w = g.graph[i] 
			# u-*1* because the graph's keys start from 1
			comp1 = find(parent, u-1) 
			comp2 = find(parent ,v-1) 

			# If two corners of current edge belong to 
			# same component, ignore current edge. Else check if 
			# current edge is closer to previous 
			# cheapest edges of comp1 and comp2 
			if comp1 != comp2:	 
				
				if cheapest[comp1] == -1 or cheapest[comp1][2] > w : 
					cheapest[comp1] = [u,v,w] 

				if cheapest[comp2] == -1 or cheapest[comp2][2] > w : 
					cheapest[comp2] = [u,v,w] 

		# Consider the above picked cheapest edges and add them 
		# to MST 
		for node in range(g.V): 

			#Check if cheapest for current set exists 
			if cheapest[node] != -1: 
				u,v,w = cheapest[node] 
				comp1 = find(parent, u-1) 
				comp2 = find(parent ,v-1) 

				if comp1 != comp2 : 
					MSTweight += w 
					union(parent, rank, comp1, comp2) 
					# print ("Edge %d-%d with weight %d included in MST" % (u,v,w)) 
					mst[u][v] = mst[v][u] = w
					numTrees = numTrees - 1
		
		#reset cheapest array 
		cheapest =[-1] * g.V 
	last = time.time() - start_time
	print("boruvska --- {0:.5f} seconds ---".format(last))

	print ("Weight of MST is %.2f" % MSTweight) 
	return mst
								
