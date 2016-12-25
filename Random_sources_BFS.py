#!/usr/bin/python2

import sys
from printStatistics import *
import random
import os

from snap import *


def process_nodes(nodes):
    global graph
    global isDirected

    out_list = [0]

    for node in nodes:
        output = TIntPrV()
        GetNodesAtHops(graph, node, output, isDirected)

        for pair in output:
            if pair.GetVal1() >= len(out_list):
                out_list += [0] * (pair.GetVal1() - len(out_list) + 1)

            out_list[pair.GetVal1()] += pair.GetVal2()

    return out_list

random.seed(os.urandom(4))

if len(sys.argv) < 3:
    error('Please give the file name and the accuracy parameter')

filename = sys.argv[1]
samples_count = int(sys.argv[2]) # Number of samples for estimation

FIn = TFIn(filename)
graph = TNGraph.Load(FIn)

# Directed graph if strongly connected, else undirected
isDirected = "lscc" in filename

samples = []
for i in xrange(samples_count):
    samples.append(random.randint(0, graph.GetNodes() - 1))

distance_histogram = process_nodes(samples)

print(distance_histogram)
printStatistics(distance_histogram, accuracy=samples_count)