import sys
import io
import snap
import numpy as np

from snap import *
from UnionFind import *


if len(sys.argv) < 2:
    error('No filename given')

filename = sys.argv[1]

samples = 100   #number of random samples for testing

FIn = snap.TFIn(filename)
Graph = snap.TNGraph.Load(FIn)
directedOrNot = True #Whether the edges are considered directed or undirected, initialization

#Directed graph if strongly connected, else undirected
if ("lscc" in str(filename)): directedOrNot = True
else: directedOrNot = False

#calculate distances between sampled pairs
distances = []
a = 0
b = 0

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
print("Approximate median distance: "+ str(median_distance))
print("Approximate mean distance: "+ str(mean_distance))
print("Approximate diameter: "+ str(diameter))
print("Approximate effective diameter: "+ str(eff_diameter))
