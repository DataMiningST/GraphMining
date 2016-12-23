#!/bin/bash

COMMAND=$1
RESULTS_DIR=./results

for file in ./data/*.txt; do
	filename=$(basename $filename)
	./$COMMAND "$file-lwcc.graph" > "$RESULTS_DIR/$filename-undirected.txt" &
	./$COMMAND "$file-lscc.graph" > "$RESULTS_DIR/$filename-directed.txt" &
done

wait
