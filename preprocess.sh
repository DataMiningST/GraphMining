#!/bin/bash

for file in ./data/*.txt; do
	./lwcc.py "$file"
	./lscc.py "$file"
done
