from snap import *

def compressIds(graph):
    result = TNGraph(graph.GetNodes(), graph.GetEdges())
    dictionary = {}
    count = 0
    
    for node in graph.Nodes():
        dictionary[node.GetId()] = count
        result.AddNode(count)
        count += 1
    
    for edge in graph.Edges():
        result.AddEdge(dictionary[edge.GetSrcNId()], dictionary[edge.GetDstNId()])
    
    return result
