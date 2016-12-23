#!/bin/bash

mkdir -p ./data

wget "http://snap.stanford.edu/data/wiki-Vote.txt.gz" -P ./data
wget "http://snap.stanford.edu/data/soc-Epinions1.txt.gz" -P ./data
wget "http://snap.stanford.edu/data/gplus_combined.txt.gz" -P ./data
wget "http://snap.stanford.edu/data/soc-pokec-relationships.txt.gz" -P ./data
wget "http://snap.stanford.edu/data/soc-LiveJournal1.txt.gz" -P ./data

for file in data/*.gz; do
	gzip -d "$file"
done

./compressTxtIds.py data/gplus_combined.txt
rm data/gplus_combined.txt
mv data/gplus_combined-c.txt data/gplus_combined.txt
