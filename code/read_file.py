#Reads and creates the graph from a txt.file 

import random
from graph import Graph

def read(file):
	with open(file, 'r') as f:
		line = f.readline().rstrip()

		while (line!=''):  #skip the intro
			line = f.readline().rstrip()

		line = f.readline().rstrip()
		dict_graph = {}
		
		while line: 
			line = line.split(" ",1)
			dict_graph[int(line[0])] = {}
			neighbors = line[1].strip('][').split(', ') 

			for elm in neighbors:
				try:
					dict_graph[int(line[0])][int(elm)] = dict_graph[int(elm)][int(line[0])]	
				except KeyError:
					dict_graph[int(line[0])][int(elm)] = round(random.uniform(0, 1),2)

			line = f.readline().rstrip()

		# print("[Read OK]")

		return dict_graph
				
