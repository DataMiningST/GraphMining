#!/usr/bin/python2

import sys

from snap import *
from printStatistics import *

from joblib import Parallel, delayed
import multiprocessing


def process_node(node):
    global graph
    global isDirected

    output = TIntPrV()
    GetNodesAtHops(graph, node, output, isDirected)

    out_list = [0] * output.Len()

    for pair in output:
        if pair.GetVal1() >= len(out_list):
            out_list += [0] * (pair.GetVal1() - len(out_list) + 1)

        out_list[pair.GetVal1()] += pair.GetVal2()

    return out_list


if len(sys.argv) < 2:
    raise Exception('Missing arguments. Please give filename.')

filename = sys.argv[1]

isDirected = "lscc" in str(filename)

inStream = TFIn(filename)
graph = TNGraph.Load(inStream)

# Calculate distance histogram by making a full BFS for every node

num_cores = multiprocessing.cpu_count()
pool = multiprocessing.pool.ThreadPool(processes=num_cores)

inputs = []
for node in graph.Nodes():
    inputs += [node.GetId()]

results = pool.map(process_node, inputs)

print(results)

distanceHistogram = []
for hist in results:
    if len(hist) >= len(distanceHistogram):
        distanceHistogram += [0] * (len(hist) - len(distanceHistogram) + 1)

    for i in xrange(len(hist)):
        distanceHistogram[i] += hist[i]

print(distanceHistogram)

printStatistics(distanceHistogram)


