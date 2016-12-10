#!/usr/bin/python2

import sys
import io

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

if len(sys.argv) < 2:
    error('No filename given')

filename = sys.argv[1]

graph = LoadEdgeList(PNGraph, filename, 0, 1)
print('Nodes: ' + str(graph.GetNodes()))
print('Edges: ' + str(graph.GetEdges()))

computeLWCCInplace(graph)
print('Nodes: ' + str(graph.GetNodes()))
print('Edges: ' + str(graph.GetEdges()))

savefilename = filename + '-lwcc.graph'
out = TFOut(savefilename)
graph.Save(out)
out.Flush()
