HOW TO RUN OUR PROJECT

1. GET THE DATA
    Either run ./get_data.sh to download, unzip and prepare the files.
    Or, if you have the .txt-files already, place them in the ./data directory manually.
    If you have not preprocessed the Google+ data, then run `./compressTxtIds.py data/gplus_combined.txt`, and delete the input file afterwards.

2. PREPOCESS THE DATA
    Run `./preprocess.sh`. This should not take longer than half an hour. It just computes the LSCCs and LWCCs.

3. COMPUTE THE ACCURATE STATISTICS
    As this can take very long, it is manual. Run `log_results.sh ./accurateStatistics.py <path>`, where path is for example `wiki-Vote.txt`. It will take the LSCC and LWCC and compute the statistics. The script is parallelized to be fast. The statistics will appear in the `./results` directory.
