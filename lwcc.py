#!/usr/bin/python2

import sys
import io

from snap import *


def computeLWCCInplace(graph):
    print('Computing largest weakly connected component...')
    components = TCnComV()
    GetWccs(graph, components)
    
    lwcc = TCnComV()
    
    # Search largest WCC
    for wcc in components:
        if lwcc.Len() < wcc.Len():
            lwcc = wcc
            
    # Convert WCC to node id set
    lwcc = frozenset(lwcc)
    
    # Delete nodes not belonging to LWCC
    for node in graph.Nodes():
        if not node.GetId() in lwcc:
            graph.DelNode(node.GetId())

    graph.Defrag()
    print('Computed largest weakly connected component.')

if len(sys.argv) < 2:
    raise Exception('No filename given')

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
