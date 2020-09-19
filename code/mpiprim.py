import time
from mpi4py import MPI
import heapq
from read_file import *
import os

def update_edges_local(edges_local_initial, edges_local, isInMST):
    for edge in edges_local.copy():
        frm = edge[1]
        to = edge[2]
        if (not isInMST[frm]) and (not isInMST[to]):
            edge[0] = float('inf')
        elif isInMST[frm] and isInMST[to]:
            edges_local.remove(edge)
        else:
            edge[0] = edges_local_initial[(frm, to)]

def main(*args):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    in_graph = {}
    if rank == 0:
        script_dir = os.path.dirname(__file__) 
        if len(args) == 0:
            print('No arguments passed, default test file ER100.txt is then used')
            rel_path = "test_files/ER100.txt"
        else:
            rel_path = args[0]
        abs_file_path = os.path.join(script_dir, rel_path)
        in_graph = read(abs_file_path)


    graph = comm.bcast(in_graph)
    
    n = len(graph)
    isInMST = [False for i in range(n)]
    isInMST[0] = True # we start from vertex 0
    target = -1 #which processor should be changing its edges_local
    offset = int(next(iter(graph)))
    edgesMST = {(int(key)-offset):{} for key in graph.keys()}
    edges_local_initial = {
        (int(frm)-offset,int(to)-offset):cost
        for frm, todict in graph.items()
        for to, cost in todict.items()
        if int(frm)-offset>=rank*(1+n//size) and int(frm)-offset<(rank+1)*(1+n//size)
    }
    edges_local = [
        [cost, frm, to]
        for (frm, to),cost in edges_local_initial.items()
        if frm < to
    ]

    if rank == 0:
        start = time.time()

    while not all(isInMST):
        update_edges_local(edges_local_initial, edges_local, isInMST)
        heapq.heapify(edges_local)
        if len(edges_local) == 0:
            edges_local.append([float('inf'), 0, 0])

        minedge_local = heapq.heappop(edges_local)

        minedge_global = comm.reduce(minedge_local, op=MPI.MIN)

        if rank == 0:
            cost, frm, to = minedge_global
            isInMST[to] = isInMST[frm] = True
            edgesMST[to][frm] = edgesMST[frm][to] = cost
            target = min(frm//(1+n//size),size-1)

        target = comm.bcast(target)

        if rank != target:
            heapq.heappush(edges_local, minedge_local)

        target = -1

        isInMST = comm.bcast(isInMST)
        edgesMST = comm.bcast(edgesMST)
    
    if rank == 0:
        mst = { str(frm+offset):{str(to+offset):cost for to,cost in todict.items()} for frm, todict in edgesMST.items()}
        print('MPIprim elapsed time for file '+rel_path, time.time()-start)
        
        total_weight = 0

        for source, neighbors in mst.items():
                    for target in neighbors:
                        total_weight+=neighbors[target]
        print("--> Weight of the mpiPrim MST = " + str(round(total_weight/2,2)))
        
        return mst, time.time()-start
    MPI.Finalize()

if __name__ == "__main__":
    main()
    SystemExit
