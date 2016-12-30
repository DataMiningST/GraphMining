HOW TO RUN OUR PROJECT

1. GET THE DATA
    Either run ./get_data.sh to download, unzip and prepare the files.
    Or, if you have the .txt-files already, place them in the ./data directory manually.
    If you have not preprocessed the Google+ data, then run `./compressTxtIds.py data/gplus_combined.txt`, and delete the input file afterwards.

2. PREPOCESS THE DATA
    Run `./preprocess.sh`. This should not take longer than half an hour. It just computes the LSCCs and LWCCs.

3. COMPUTE THE ACCURATE STATISTICS
    As this can take very long, it is manual. Run `log_results.sh ./accurateStatistics.py <path>`, where path is for example `./data/wiki-Vote.txt`. It will take the LSCC and LWCC and compute the statistics. The script is parallelized to be fast. The statistics will appear in the `./results` directory. If you don't have enough RAM, the programs might throw bad_alloc exceptions. 16GB should be enough.

4. COMPUTE THE APPROXIMATE STATISTICS
    The scripts for the random sampling and random source bfs approximations are called Random_sample.py and Random_sources_BFS.py. They are used with `./<script> <path> <accuracy>`. Path is the same as in 3., and accuracy is the accuracy parameter. It controls the amount of pairs that should be sampled for the first script, and the amount of nodes that should be sampled as BFS sources for the second script. For the Flajolet-Marten algorithm, there exists a cpp program that needs to be compiled first. To compile this, first, snap needs to be compiled. Change into the Snap-3.0 directory and run make. After the command completed change back into the super directory, and run make again. Then you can use `./fms <path> <accuracy>` to approximate the statistics with Flajolet-Marten. In this case, <accuracy> is the number of counters that should be used for every node.
    To execute the tests we used for our report, execute script question2.2.sh and wait for a day or so.
