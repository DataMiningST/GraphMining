#!/usr/bin/python2

import sys
import io
import snap
import numpy as np

from snap import *


if len(sys.argv) < 3:
    error('Please give the file name and the accuracy parameter')

filename = sys.argv[1]
samples = int(sys.argv[2]) # Number of samples for estimation

FIn = snap.TFIn(filename)
Graph = snap.TNGraph.Load(FIn)

#Directed graph if strongly connected, else undirected
directedOrNot = "lscc" in str(filename)

#calculate distances between sampled pairs
distances = []

for x in range(0, samples):
    a = Graph.GetRndNId()
    b = Graph.GetRndNId()
    length = GetShortPath(Graph, a, b, directedOrNot)
    distances.append(length)

distances = sorted(distances)


median_distance = distances[(samples)/2]
mean_distance = np.mean(distances)
diameter = np.max(distances)
eff_diameter = distances[(samples)*9/10]

print("Random pair sampling (" + str(samples) + " samples):")
print("Approximate median distance: " + str(median_distance))
print("Approximate mean distance: " + str(mean_distance))
print("Approximate diameter: " + str(diameter))
print("Approximate effective diameter: " + str(eff_diameter))
