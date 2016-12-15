#!/usr/bin/python2

import sys

from snap import *
from printStatistics import *

if len(sys.argv) < 3:
    raise Exception('Missing arguments. Please give filename and true/false if graph is directed')

filename = sys.argv[1]
if sys.argv[2].lower() == 'true':
    isDirected = True
elif sys.argv[2].lower() == 'false':
    isDirected = False
else:
    raise Exception('Please give either true or false as second argument to indicate if the graph should be viewed as directed or not')

inStream = TFIn(filename)
graph = TNGraph.Load(inStream)

# Calculate distance histogram by making a full BFS for every node

upperDiameterBound = GetBfsFullDiam(graph, 1, isDirected) * 2
distanceHistogram = [0] * (upperDiameterBound + 1)
print('Upper bound for diameter: ' + str(upperDiameterBound))

for node in graph.Nodes():
    output = TIntPrV()
    GetNodesAtHops(graph, node.GetId(), output, isDirected)

    for distance in output:
        if distance.GetVal1() >= len(distanceHistogram):
            distanceHistogram += [0] * (distance.GetVal1() - len(distanceHistogram) + 1)

        distanceHistogram[distance.GetVal1()] += distance.GetVal2()

print(distanceHistogram)

printStatistics(distanceHistogram)
