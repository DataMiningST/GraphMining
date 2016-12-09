#!/bin/python2

from snap import *
from UnionFind import *


def computeLWCCInplace(graph):
    print('Computing largest weakly connected component...')
    uf = UnionFind()
    marked = set()

    for edge in graph.Edges():
        (source, destination) = edge.GetId()
        uf.union(source, destination)

    # Find weakly connected component with maximum size
    ccSizes = {}
    maxid = None
    maxn = 0

    for node in graph.Nodes():
        nid = uf[node.GetId()]

        if nid in ccSizes:
            ccSizes[nid] += 1

            if ccSizes[nid] > maxn:
                maxid = nid
                maxn = ccSizes[nid]
        else:
            ccSizes[nid] = 1

            if maxid == None:
                maxid = nid
                maxn = 1

    for node in graph.Nodes():
        nid = uf[node.GetId()]

        if nid != maxid:
            graph.DelNode(node.GetId())

    graph.Defrag()
    print('Computed largest weakly connected component.')


graph = LoadEdgeList(PNGraph, "wiki-Vote.txt", 0, 1)
print(graph.GetNodes())
print(graph.GetEdges())

computeLWCCInplace(graph)

print(graph.GetNodes())
print(graph.GetEdges())
