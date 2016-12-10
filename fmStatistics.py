#!/usr/bin/python2

import sys
import io
import random

from snap import *
from FMCounter import FMCounter
from copy import copy

counterWidth = 64 # 64 bit is most modern systems word width
ncounters = 64 # Value used in paper, gives average error < 10%
maxDistance = 11 # Cap for the maximum distance checked. Don't know how to automate this yet.

if len(sys.argv) < 2:
    raise Exception('No filename given')

filename = sys.argv[1]

inStream = TFIn(filename)
graph = TNGraph.Load(inStream)

# Initialize counters

currentCounters = [0] * graph.GetNodes()
lastCounters = [0] * graph.GetNodes()

for i in xrange(0, len(currentCounters)):
    currentCounters[i] = FMCounter(ncounters, counterWidth)
    currentCounters[i].initialize()

distances = [0] * (maxDistance + 1)

for distance in xrange(1, maxDistance + 1):
    for i in xrange(0, len(currentCounters)):
        lastCounters[i] = currentCounters[i].copy()

    for edge in graph.Edges():
        currentCounters[edge.GetSrcNId()].union(lastCounters[edge.GetDstNId()])
    
    for counter in currentCounters:
        distances[distance] += counter.evaluate(True)
        
nodePairsWithDistance = [0] * maxDistance
for distance in xrange(1, maxDistance):
    nodePairsWithDistance[distance] = (distances[distance + 1] - distances[distance])

print("Node pairs found: " + str(distances[maxDistance]) + "/" + str(graph.GetNodes()**2))
print(nodePairsWithDistance)
