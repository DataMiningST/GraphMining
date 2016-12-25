#!/usr/bin/python2

import sys

from snap import *
from printStatistics import *

from joblib import Parallel, delayed
import multiprocessing

import time


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


if len(sys.argv) < 2:
    raise Exception('Missing arguments. Please give filename.')

filename = sys.argv[1]

isDirected = "lscc" in filename

inStream = TFIn(filename)
graph = TNGraph.Load(inStream)

# Calculate distance histogram by making a full BFS for every node

start_time = time.time()

num_cores = multiprocessing.cpu_count()
pool = multiprocessing.pool.ThreadPool(processes=num_cores)

inputs = []
for node in graph.Nodes():
    inputs += [node.GetId()]

sliced_inputs = [None] * num_cores
for i in xrange(num_cores):
    sliced_inputs[i] = inputs[i * len(inputs) // num_cores:(i + 1) * len(inputs) // num_cores]

results = pool.map(process_nodes, sliced_inputs)

distanceHistogram = []
for hist in results:
    if len(hist) >= len(distanceHistogram):
        distanceHistogram += [0] * (len(hist) - len(distanceHistogram) + 1)

    for i in xrange(len(hist)):
        distanceHistogram[i] += hist[i]

duration = time.time() - start_time

print(distanceHistogram)

print("Duration: " + str(duration) + "s")
printStatistics(distanceHistogram)


