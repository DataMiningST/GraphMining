#include "Snap.h"
#include "FMCounter.h"

#include <vector>
#include <chrono>
#include <iostream>


using namespace std;
using namespace std::chrono;
using namespace TSnap;

const int abortEqualDistanceChainLength = 5;

PNGraph loadGraph(TStr& path) {
    TFIn FIn(path);
    return TNGraph::Load(FIn);
}

vector<uint64_t> anc0(PNGraph graph, bool isDirected) {
    mt19937 random(chrono::system_clock::now().time_since_epoch().count());

    // Initialize counters
    FMCounter *currentCounters = new FMCounter[graph->GetNodes()];
    FMCounter *lastCounters = new FMCounter[graph->GetNodes()];

    for (int i = 0; i < graph->GetNodes(); i++) {
	currentCounters[i].initialize(random);
    }

    vector<uint64_t> distanceSums;
    distanceSums.push_back(0);
    int equalDistanceChainLength = 0;
    bool abort = false;

    for (unsigned distance = 1; !abort; distance++) {
        for (int i = 0; i < graph->GetNodes(); i++) {
            lastCounters[i] = currentCounters[i];
	}

	for (TNGraph::TEdgeI edge = graph->BegEI(); edge != graph->EndEI(); edge++) {
	    currentCounters[edge.GetSrcNId()]._union(lastCounters[edge.GetDstNId()]);

	    if (isDirected) {
	        currentCounters[edge.GetDstNId()]._union(lastCounters[edge.GetSrcNId()]);
	    }
	}

	distanceSums.push_back(0);
        for (int i = 0; i < graph->GetNodes(); i++) {
            distanceSums[distance] += currentCounters[i].evaluate();
	}

        if (distanceSums[distance] == distanceSums[distance - 1]) {
            equalDistanceChainLength++;

            if (equalDistanceChainLength >= abortEqualDistanceChainLength) {
                abort = true;
            }
        } else {
            equalDistanceChainLength = 0;
        }
    }

    return distanceSums;
}

int main(int argc, char** argv) {
    if (argc < 2) {
	cout << "No filename given" << endl;
    }

    TStr filename(argv[1]);
    string cpp_fn(argv[1]);

    bool isDirected = cpp_fn.find("lscc");

    PNGraph graph(loadGraph(filename));

    high_resolution_clock::time_point startTime = high_resolution_clock::now();
    vector<uint64_t> distanceSums = anc0(graph, isDirected);
    high_resolution_clock::time_point endTime = high_resolution_clock::now();

    vector<uint64_t> distanceHistogram(distanceSums.size() - 1);
    for (unsigned i = 0; i < distanceHistogram.size(); i++) {
        distanceHistogram[i] = distanceSums[i + 1] - distanceSums[i];
    }

    // Print out computation statistics

    uint64_t histogramSum = distanceSums[distanceSums.size() - 1];
    int oldPrecision = cout.precision();
    cout.precision(4);
    cout << "Node pairs fraction: " << ((double) histogramSum / ((double) graph->GetNodes() * graph->GetNodes())) << endl;
    cout.precision(oldPrecision);

    cout << "Max distance checked: " << distanceSums.size() - 1 << endl;

    bool once = true;
    for (auto n: distanceHistogram) {
        if (once) {
            once = false;
        } else {
            cout << ", ";
        }

        cout << n;
    }
    cout << endl;

    // Execution time

    double duration = duration_cast<microseconds>( endTime - startTime ).count() / 1e6;
    cout << "Execution time: " << duration << "s" << endl;

    // Median distance

    uint64_t medianIndex = histogramSum / 2;
    uint64_t histogramIndex = 0;
    int median = -1;

    for (unsigned i = 0; i < distanceHistogram.size(); i++) {
        histogramIndex += distanceHistogram[i];

	if (histogramIndex >= medianIndex) {
            median = i;
            break;
        }
    }

    cout << "Median distance: " << median << endl;

    // Mean distance

    double mean = 0;

    for (unsigned i = 0; i < distanceHistogram.size(); i++) {
        mean += i * distanceHistogram[i];
    }

    mean /= histogramSum;
    cout << "Mean distance: " << mean << endl;

    // Diameter
    
    int diameter = -1;

    for (unsigned i = distanceHistogram.size() - 1; i >= 0; i--) {
        if (distanceHistogram[i] != 0) {
            diameter = i;
            break;
        }
    }

    cout << "Diameter: " << diameter << endl;

    // Effective diameter

    uint64_t edIndex = (uint64_t) (histogramSum * 0.9);
    histogramIndex = 0;
    int effectiveDiameter = -1;

    for (unsigned i = 0; i < distanceHistogram.size(); i++) {
        histogramIndex += distanceHistogram[i];

	if (histogramIndex >= edIndex) {
            effectiveDiameter = i;
            break;
        }
    }

    cout << "Effective diameter: " << effectiveDiameter << endl;
}
