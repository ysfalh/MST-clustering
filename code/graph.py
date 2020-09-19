class Graph: 

	def __init__(self, dict_graph, show = True): #dict_graph is a nested dictionary
		self.V = len(dict_graph) #No. of vertices 
		self.graph = [] # to store graph 
		self.vertices = []
		
		total_weight = 0
		n_edges = 0
		for source, neighbors in dict_graph.items():
			for target in neighbors:
				w = neighbors[target] 
				self.graph.append([source,target,w]) 
				total_weight+=w
				n_edges+=1
			self.vertices.append(source)

		if show : 
			print("=========================")
			print("Graph of " + str(self.V) + " vertices") 
			print("No. edges = " + str(n_edges//2)) 
			print("Total weight = " + str(round(total_weight/2,2)))
			print("=========================")
