#!/usr/bin/python2

import sys
import io

from snap import *
from UnionFind import *


def computeLSCCInplace(graph):
    print('Computing largest strongly connected component...')
    components = TCnComV()
    GetSccs(graph, components)
    
    lscc = TCnComV()
    
    # Search largest SCC
    for scc in components:
        if lscc.Len() < scc.Len():
            lscc = scc
            
    # Convert SCC to node id set
    lscc = frozenset(lscc)
    
    # Delete nodes not belonging to LSCC
    for node in graph.Nodes():
        if not node.GetId() in lscc:
            graph.DelNode(node.GetId())

    graph.Defrag()
    print('Computed largest strongly connected component.')

if len(sys.argv) < 2:
    error('No filename given')

filename = sys.argv[1]

graph = LoadEdgeList(PNGraph, filename, 0, 1)
print('Nodes: ' + str(graph.GetNodes()))
print('Edges: ' + str(graph.GetEdges()))

computeLSCCInplace(graph)
print('Nodes: ' + str(graph.GetNodes()))
print('Edges: ' + str(graph.GetEdges()))

savefilename = filename + '-lscc.graph'
out = TFOut(savefilename)
graph.Save(out)
out.Flush()
