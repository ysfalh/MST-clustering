from read_file import *
from kruskal import *
from kclustering import *

import sys
import os
script_dir = os.path.dirname(__file__) 


def main(argv):

	if (len(sys.argv) != 3):
		print("Usage: ", argv[0], "csv nb_clusters")
		sys.exit(1)

	rel_path = "test_datasets/" + str(sys.argv[1])
	abs_file_path = os.path.join(script_dir, rel_path)

	in_graph, points = read_csv(abs_file_path)
	total_weight = 0
	mst = KruskalMST(in_graph)	

	for source, neighbors in mst.items():
				for target in neighbors:
					total_weight+=neighbors[target]
	print("--> Weight of the MST = " + str(round(total_weight/2,2)))
	print("=========================")

	k = int(sys.argv[2])

	clusters = clustering(mst, k)
	centers, accuracy = set_centers(clusters, points)
	variances = intracluster_variance(clusters, centers, points)
	print("Clusters: ")
	for center in centers :
		center.print_point()
	print("=========================")
	print("Intracluster variance after MST clustering: ", variances)
	print("Accuracy = {:.1%}".format(accuracy))


if __name__ == "__main__":
    main(sys.argv)