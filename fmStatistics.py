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

# ANC-0 algorithm

distances = [0] * (maxDistance + 1)

for distance in xrange(1, maxDistance + 1):
    for i in xrange(0, len(currentCounters)):
        lastCounters[i] = currentCounters[i].copy()

    for edge in graph.Edges():
        currentCounters[edge.GetSrcNId()].union(lastCounters[edge.GetDstNId()])
    
    for counter in currentCounters:
        distances[distance] += counter.evaluate(True)

# Calculating distance histogram

distanceHistogram = [0] * maxDistance
for distance in xrange(1, maxDistance):
    distanceHistogram[distance] = (distances[distance + 1] - distances[distance])
histogramSum = distances[maxDistance]

print("Node pairs found: " + str(distances[maxDistance]) + "/" + str(graph.GetNodes()**2))
print(distanceHistogram)

# Calculate median distance from histogram

medianIndex = histogramSum // 2
histogramIndex = 0

for i, bucket in enumerate(distanceHistogram):
    histogramIndex += bucket
    
    if histogramIndex >= medianIndex:
        median = i
        break

print("Median distance: " + str(median))

# Calculate mean distance from histogram

mean = 0.0
for i in xrange(len(distanceHistogram)):
    mean += i * distanceHistogram[i]

mean /= histogramSum
print("Mean distance: " + str(mean))

# Diameter (= max of all distances)

for i, bucket in reversed(list(enumerate(distanceHistogram))):
    if bucket != 0:
        diameter = i
        break

print("Diameter: " + str(diameter))

# Effective diameter

edIndex = int(histogramSum * 0.9)
histogramIndex = 0

for i, bucket in enumerate(distanceHistogram):
    histogramIndex += bucket
    
    if histogramIndex >= edIndex:
        effectiveDiameter = i
        break

print("Effective diameter: " + str(effectiveDiameter))
