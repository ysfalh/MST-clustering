from graph import Graph
from point import *
from unionfind import *

def clustering(in_graph, k):  #takes the MST from the dataset transformed into graphs.

	g = Graph(in_graph, show = False)
	g.graph = sorted(g.graph,key=lambda item: item[2]) 

	parent = dict(); rank = dict()
	new_graph = g.graph[:2*(g.V-k)]  #we keep the k cheapest edges

	for vertice in g.vertices:
		parent[vertice]=vertice
		rank[vertice] = 0
	
	
	for i in range(2*(g.V-k)) : 

		u,v,w = new_graph[i] 
		i = i + 1
		x = find(parent, u) 
		y = find(parent, v) 

		if x != y: 
			union(parent, rank, x, y)	

	#Set clusters 
	root = dict(); cluster = dict()
	for vertice in g.vertices:
		pere = find(parent,vertice)
		root[vertice] = pere
		if pere in cluster:
			cluster[pere].append(vertice)	
		else :
			cluster[pere] = [vertice]

	return cluster


def set_centers(cluster, points):
	centers = []
	dim = len(points[0].coords)
	accuracy = 0

	for i,(key,value) in enumerate(cluster.items()) :
		somme = [0]*dim
		label = dict()

		for k in range(len(value)):

			numero = cluster[key][k]
			p = points[int(numero)-1]
			for m in range(dim):
				somme[m] += p.coords[m]
			
			if p.name in label : 
				label[p.name]+=1
			else :
				label[p.name] = 1

		name = max(label, key=lambda k: label[k])

		for k in range(len(value)):
			numero = cluster[key][k]
			p = points[int(numero)-1]
			if name==p.name:
				accuracy+=1

		coords = [round(somme[j]/len(value),2) for j in range(dim)]
		c = Point(str(i),dim,name)
		c.coords = coords
		centers.append(c)
	accuracy/=len(points)

	return centers, accuracy

def intracluster_variance(cluster, center, points):
	variance = 0
	dim = len(points[0].coords)
	for i,(key,value) in enumerate(cluster.items()) :

		for k in range(len(value)):

			numero = cluster[key][k]
			p = points[int(numero)-1]
			variance += p.euclidian_dist(center[i])

	variance = round(variance/len(points), 2)

	return variance



'''
New graph : 
[['1', '5', 0.14], ['5', '1', 0.14], ['3', '4', 0.24], 
['4', '3', 0.24], ['2', '3', 0.3], ['3', '2', 0.3]]
Parent : 
{'1': '1', '2': '3', '3': '3', '4': '3', '5': '1', '6': '6'}
Root (souvent différent):
{'1': '1', '2': '3', '3': '3', '4': '3', '5': '1', '6': '6'}
#Cluster : 
{'1': ['1', '5'], '3': ['2', '3', '4'], '6': ['6']}
'''