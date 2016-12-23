#!/usr/bin/python2

import sys

if len(sys.argv) < 2:
    raise Exception('Missing arguments. Please give filename.')

filename = sys.argv[1]
resultfilename = filename[:-4] + "-c.txt"

ids = {}
cur_id = 0

with open(filename) as f, open(resultfilename, "w") as resultfile:
    for line in f:
        line = line.strip()

        if line.startswith("#"):
            continue

        raw_ids = line.split(" ")

        for i in xrange(2):
            if raw_ids[i] not in ids.keys():
                ids[raw_ids] = cur_id
                cur_id += 1

        resultfile.write(ids[raw_ids[0]] + " " + ids[raw_ids[1]] + "\n")