import sys
import io
import snap
import numpy as np

from snap import *
from UnionFind import *

if len(sys.argv) < 2:
    error('No filename given')

filename = sys.argv[1]

FIn = snap.TFIn(filename)
Graph = snap.TNGraph.Load(FIn)

samples = 100   #number of random samples for testing
directedOrNot = True #Whether the edges are considered directed or undirected, initialization

#Directed graph if strongly connected, else undirected
if ("lscc" in str(filename)): directedOrNot = True
else: directedOrNot = False

nodes = Graph.GetNodes()
#previous attempts
#diameter = snap.GetBfsFullDiam(Graph, samples, directedOrNot)
#print ("Approximate diameter: "+ str(diam))

#eff_diameter = snap.GetBfsEffDiam(Graph, samples, directedOrNot)
#print ("Approximate effective diameter: "+ str(effdiam))

#calculate BFS for random sources
med_distances = []
mea_distances = []
diam_distances = []
eff_distances = []

current_distribution = []

a = 0
m = 0


for x in range(0, samples):
    current_distrib = []
    a = Graph.GetRndNId()
    hasht = snap.TIntH()
    length = GetShortPath(Graph, a, hasht, directedOrNot) #distance to the furthest-away node from a
    
    for y in range(0, length):
        NodeV = snap.TIntV()
        m = GetNodesAtHop(Graph, a, y, NodeV, directedOrNot)
        current_distribution.extend([y+1 for z in range(m)]) #adds a value to the list for each node that is at distance y+1
    
    med_distances.append(current_distribution[nodes/2])
    mea_distances.append(np.mean(current_distribution))
    diam_distances.append(length)
    eff_distances.append(current_distribution[nodes*9/10])
    
med_distances = sorted(med_distances)
mea_distances = sorted(mea_distances)
diam_distances = sorted(diam_distances)
eff_distances = sorted(eff_distances)

median_distance = med_distances[(samples)/2]
mean_distance = np.mean(mea_distances)
diameter = np.max(diam_distances)
eff_diameter = eff_distances[(samples)/2]

print("BFS search for random sources (" + str(samples) + " samples):")
print("Approximate median distance: "+ str(median_distance))
print("Approximate mean distance: "+ str(mean_distance))
print("Approximate diameter: "+ str(diameter))
print("Approximate effective diameter: "+ str(eff_diameter))