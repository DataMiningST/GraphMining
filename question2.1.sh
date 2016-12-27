#!/bin/bash

COMMAND=$1
RESULTS_DIR=./results

for file in ./data/*.txt; do
	filename=$(basename $file)
	./Random_sample.py "$file-lwcc.graph" 16384 > "$RESULTS_DIR/$filename-RS-undirected.txt" &
	./Random_sample.py "$file-lscc.graph" 16384 > "$RESULTS_DIR/$filename-RS-directed.txt" &

	./Random_sources_BFS.py "$file-lwcc.graph" 1024 > "$RESULTS_DIR/$filename-RBFS-undirected.txt" &
	./Random_sources_BFS.py "$file-lscc.graph" 1024 > "$RESULTS_DIR/$filename-RBFS-directed.txt" &

	./fms "$file-lwcc.graph" 64 > "$RESULTS_DIR/$filename-FM-undirected.txt" &
	./fms "$file-lscc.graph" 64 > "$RESULTS_DIR/$filename-FM-directed.txt" &

	wait
done
