# Minimum Spanning Trees based clustering technique
INF442 Project: Minimum Spanning Trees (MST)
-- Y.Allouah and J.Sroussi --

To read the project's description, please open "p3-mst.pdf" file in the main directory.
To read the project's report of the solution we implemented, please open "report_mstc_english.pdf" in main directory.

The source code is located in the \code folder, along with the graphs used for our tests.

1. In order to test an algorithm named "*alg*", you need to run the file named "*alg*_test", which is a python script except for the parallel prim algorithm (of source code "mpiprim.py"). For the latter, the test file is a .bat windows batch file. 

If it does not work on your computer, please run: "mpiexec -np 4 python mpiprim.py" in your command shell. Make sure an MPI environment is installed on your computer. Also, you can use any other number of processes instead of 4. If the message "No arguments passed on the command line" is displayed, your system is not passing arguments to Python through the command line. You will then see a default test of 4 parallel processes on a graph of 100 vertices. If you want to test on another file, please then run the mpiprim_pythontest.py script but this will use only one process as the only was to specify the number of processes is through the command line.

2. Exceptions : 

kclustering_test.py: 
To execute, format is: kclustering_test.py csv nb_clusters
Ex: kclustering_test.py iris.csv 3
	
kmeans.cpp: 
Call "make kmeans.cpp" in terminal. 
To execute, format is: ./kmeans csv nb_clusters 
Ex: ./kmeans iris_space.csv 3
NB: use dataset with space delimiters (such as iris_space.csv)

3. To test functions with:
- .txt files: files must be in the "test_files" folder
- .csv files: files must be in the "test_datasets" folder
