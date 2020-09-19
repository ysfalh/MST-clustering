import heapq
import random
import time


def prim(graph):
    starting_vertex = random.choice(list(graph.keys())) #we could choose any vertex
    mst = {key : dict() for key in graph.keys()}
    visited = set([starting_vertex])
    edges = [
        (cost, starting_vertex, to)
        for to, cost in graph[starting_vertex].items()
    ]
    heapq.heapify(edges)

    start_time = time.time()

    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst[frm][to] = mst[to][frm] = cost
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heapq.heappush(edges, (cost, to, to_next))

    last = time.time() - start_time
    print("--- {0:.5f} seconds ---".format(last))

    return mst, last
