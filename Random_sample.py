#!/usr/bin/python2

import sys
import io
from printStatistics import *

from snap import *


if len(sys.argv) < 3:
    error('Please give the file name and the accuracy parameter')

filename = sys.argv[1]
samples = int(sys.argv[2]) # Number of samples for estimation

FIn = TFIn(filename)
Graph = TNGraph.Load(FIn)

#Directed graph if strongly connected, else undirected
directedOrNot = "lscc" in filename

#calculate distances between sampled pairs
distance_histogram = []

for x in range(0, samples):
    a = Graph.GetRndNId()
    b = Graph.GetRndNId()
    distance = GetShortPath(Graph, a, b, directedOrNot)

    if len(distance_histogram) <= distance:
        distance_histogram += [0] * (distance - len(distance_histogram) + 1)

    distance_histogram[distance] += 1

print(distance_histogram)
printStatistics(distance_histogram, accuracy=samples)