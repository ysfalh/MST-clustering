
from read_file import *
from boruvska import *
from kruskal import *

import os
script_dir = os.path.dirname(__file__) 

def boruvska_test(file):
	
	rel_path = r"test_files/"+file
	abs_file_path = os.path.join(script_dir, rel_path)

	in_graph = read(abs_file_path)
	total_weight = 0

	mst, last = KruskalMST(in_graph)
	for source, neighbors in mst.items():
				for target in neighbors:
					total_weight+=neighbors[target]
	print("--> Weight of the Kruskal MST = " + str(round(total_weight/2,2)))
	total_weight = 0
	mst= boruvska(in_graph)
	
	for source, neighbors in mst.items():
				for target in neighbors:
					total_weight+=neighbors[target]
	print("--> Weight of the Boruvska MST = " + str(round(total_weight/2,2)))

	return mst, last


test_list = ["ER25.txt", "ER50.txt", "ER100.txt",
			"ER150.txt", "ER200.txt", "ER250.txt",
			"ER300.txt", "ER500.txt", "ER1000.txt"]

for file in test_list :
	boruvska_test(file)



"""
example_graph = {
    'A': {'B': 2, 'C': 3},
    'B': {'A': 2, 'C': 1, 'D': 1, 'E': 4},
    'C': {'A': 3, 'B': 1, 'F': 5},
    'D': {'B': 1, 'E': 1},
    'E': {'B': 4, 'D': 1, 'F': 1},
    'F': {'C': 5, 'E': 1, 'G': 1},
    'G': {'F': 1},
}
"""
