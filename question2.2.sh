#!/bin/bash

DATA=./data/gplus_combined.txt
RS_VALUES="1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768"
RBFS_VALUES="1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768"
FM_VALUES="1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192"

echo "" > results/$(basename $DATA)-RS-undirected-multi.txt
echo "" > results/$(basename $DATA)-RS-directed-multi.txt
echo "" > results/$(basename $DATA)-RBFS-undirected-multi.txt
echo "" > results/$(basename $DATA)-RBFS-directed-multi.txt
echo "" > results/$(basename $DATA)-FM-undirected-multi.txt
echo "" > results/$(basename $DATA)-FM-directed-multi.txt

for acc in $RS_VALUES; do
	./Random_sample.py $DATA-lwcc.graph $acc >> results/$(basename $DATA)-RS-undirected-multi.txt &
	./Random_sample.py $DATA-lscc.graph $acc >> results/$(basename $DATA)-RS-directed-multi.txt &

	wait
done

for acc in $RBFS_VALUES; do
	./Random_sources_BFS.py $DATA-lwcc.graph $acc >> results/$(basename $DATA)-RBFS-undirected-multi.txt &
	./Random_sources_BFS.py $DATA-lscc.graph $acc >> results/$(basename $DATA)-RBFS-directed-multi.txt &

	wait
done

for acc in $FM_VALUES; do
	./fms $DATA-lwcc.graph $acc >> results/$(basename $DATA)-FM-undirected-multi.txt &
	./fms $DATA-lscc.graph $acc >> results/$(basename $DATA)-FM-directed-multi.txt &

	wait
done
