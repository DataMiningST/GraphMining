#!/bin/bash

COMMAND=$1
FILE=$2
RESULTS_DIR=./results
FILENAME=$(basename $FILE)

mkdir -p "$RESULTS_DIR"

./$COMMAND "$FILE-lscc.graph" > "$RESULTS_DIR/$FILENAME-directed.txt"
./$COMMAND "$FILE-lwcc.graph" > "$RESULTS_DIR/$FILENAME-undirected.txt"
