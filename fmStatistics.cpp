#include "Snap.h"
#include "FMCounter.h"

#include <vector>
#include <chrono>
#include <iostream>
#include <cstdlib>
#include <limits>


using namespace std;
using namespace std::chrono;
using namespace TSnap;

const int abortEqualDistanceChainLength = 1;

PNGraph loadGraph(TStr& path) {
    TFIn FIn(path);
    return TNGraph::Load(FIn);
}

vector<uint64_t> anc0(PNGraph graph, unsigned minIterations, unsigned maxIterations, bool isDirected, const unsigned accuracy) {
    mt19937 random(chrono::system_clock::now().time_since_epoch().count());

    // Initialize counters
    FMCounter counter(accuracy);

    uint32_t *currentCounters = (uint32_t*) malloc(graph->GetNodes() * accuracy * sizeof(uint32_t));
    uint32_t *lastCounters = (uint32_t*) malloc(graph->GetNodes() * accuracy * sizeof(uint32_t));

    for (int i = 0; i < graph->GetNodes(); i++) {
        counter.initialize(random, currentCounters + i * accuracy);
    }

    vector<uint64_t> distanceSums;
    distanceSums.push_back(graph->GetNodes());
    int equalDistanceChainLength = 0;
    bool abort = false;

    for (unsigned distance = 1; !abort; distance++) {
        memcpy(lastCounters, currentCounters, graph->GetNodes() * accuracy * sizeof(uint32_t));

        for (TNGraph::TEdgeI edge = graph->BegEI(); edge != graph->EndEI(); edge++) {
            counter._union(currentCounters + edge.GetSrcNId() * accuracy, lastCounters + edge.GetDstNId() * accuracy);

            if (!isDirected) {
                counter._union(currentCounters + edge.GetDstNId() * accuracy, lastCounters + edge.GetSrcNId() * accuracy);
            }
        }

        distanceSums.push_back(0);
        for (int i = 0; i < graph->GetNodes(); i++) {
            distanceSums[distance] += counter.evaluate(currentCounters + i * accuracy);
        }

        if (distance >= maxIterations) {
            abort = true;
        }

        if (distanceSums[distance] == distanceSums[distance - 1]) {
            equalDistanceChainLength++;

            if (equalDistanceChainLength >= abortEqualDistanceChainLength && distance >= minIterations) {
                abort = true;
            }
        } else {
            equalDistanceChainLength = 0;
        }
    }

    free(currentCounters);
    free(lastCounters);

    return distanceSums;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        cout << "Please give the filename and the accuracy parameter as program arguments" << endl;
    }

    TStr filename(argv[1]);
    string cpp_fn(argv[1]);

    bool isDirected = cpp_fn.find("lscc");
    unsigned accuracy = atoi(argv[2]);

    cout << "Accuracy: " << accuracy << endl;
    cout << "Directed mode: " << isDirected << endl;

    PNGraph graph(loadGraph(filename));

    unsigned minIterations = numeric_limits<unsigned>::min();
    unsigned maxIterations = numeric_limits<unsigned>::max();

    if (!isDirected) {
        maxIterations = GetBfsFullDiam(graph, 1, false);
    }

    high_resolution_clock::time_point startTime = high_resolution_clock::now();
    vector<uint64_t> distanceSums = anc0(graph, minIterations, maxIterations, isDirected, accuracy);
    high_resolution_clock::time_point endTime = high_resolution_clock::now();

    vector<uint64_t> distanceHistogram(distanceSums.size());
    for (unsigned i = 0; i < distanceHistogram.size() - 1; i++) {
        distanceHistogram[i + 1] = distanceSums[i + 1] - distanceSums[i];
    }
    distanceHistogram[0] = graph->GetNodes();

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
