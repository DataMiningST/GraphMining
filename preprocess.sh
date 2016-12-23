#!/bin/bash

mkdir -p ./results

for file in ./data/*.txt; do
	basename=$(basename $file)
	./lwcc.py "$file" > "/tmp/$basename-lwcc" &
	./lscc.py "$file" > "/tmp/$basename-lscc" &
done

wait

OUT="results/preprocessing.txt"

for file in ./data/*.txt; do
	basename=$(basename $file)
	echo "$file" >> $OUT
	echo "LWCC:" >> $OUT
	cat "/tmp/$basename-lwcc" >> $OUT
	echo "LSCC:" >> $OUT
	cat "/tmp/$basename-lscc" >> $OUT
done
