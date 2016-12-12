#include "Snap.h"
#include "FMCounter.h"

#include <vector>
#include <chrono>
#include <iostream>


using namespace std;
using namespace TSnap;

const int maxDistance = 11; // Cap for the maximum distance checked. Don't know how to automate this yet.

PNGraph loadGraph(TStr& path) {
    TFIn FIn(path);
    return TNGraph::Load(FIn);
}

vector<uint32_t> anc0(PNGraph graph) {
    mt19937 random(chrono::system_clock::now().time_since_epoch().count());

    // Initialize counters
    FMCounter *currentCounters = new FMCounter[graph->GetNodes()];
    FMCounter *lastCounters = new FMCounter[graph->GetNodes()];

    for (int i = 0; i < graph->GetNodes(); i++) {
	currentCounters[i].initialize(random);
    }

    vector<uint32_t> distanceSums(maxDistance + 1);
    distanceSums[0] = 0;

    for (int distance = 1; distance < distanceSums.size(); distance++) {
        for (int i = 0; i < graph->GetNodes(); i++) {
            lastCounters[i] = currentCounters[i];
	}

	for (TNGraph::TEdgeI edge = graph->BegEI(); edge != graph->EndEI(); edge++) {
	    currentCounters[edge.GetSrcNId()]._union(lastCounters[edge.GetDstNId()]);
	}

	distanceSums[distance] = 0;
        for (int i = 0; i < graph->GetNodes(); i++) {
            distanceSums[distance] += currentCounters[i].evaluate();
	}
    }

    return distanceSums;
}

int main(int argc, char** argv) {
    if (argc < 2) {
	cout << "No filename given" << endl;
    }

    TStr filename(argv[1]);

    PNGraph graph(loadGraph(filename));
    vector<uint32_t> distanceSums = anc0(graph);
    vector<uint32_t> distanceHistogram(distanceSums.size() - 1);

    for (int i = 0; i < distanceHistogram.size(); i++) {
        distanceHistogram[i] = distanceSums[i + 1] - distanceSums[i];
    }

    // Print out computation statistics

    uint32_t histogramSum = distanceSums[maxDistance];
    cout << "Node pairs found: " << histogramSum << "/" << (graph->GetNodes() * graph->GetNodes()) << endl;

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

    // Median distance

    uint32_t medianIndex = histogramSum / 2;
    uint32_t histogramIndex = 0;
    int median = -1;

    for (int i = 0; i < distanceHistogram.size(); i++) {
        histogramIndex += distanceHistogram[i];

	if (histogramIndex >= medianIndex) {
            median = i;
            break;
        }
    }

    cout << "Median distance: " << median << endl;

    // Mean distance

    double mean = 0;

    for (int i = 0; i < distanceHistogram.size(); i++) {
        mean += i * distanceHistogram[i];
    }

    mean /= histogramSum;
    cout << "Mean distance: " << mean << endl;

    // Diameter
    
    int diameter = -1;

    for (int i = distanceHistogram.size() - 1; i >= 0; i--) {
        if (distanceHistogram[i] != 0) {
            diameter = i;
            break;
        }
    }

    cout << "Diameter: " << diameter << endl;

    // Effective diameter

    uint32_t edIndex = (uint32_t) (histogramSum * 0.9);
    histogramIndex = 0;
    int effectiveDiameter = -1;

    for (int i = 0; i < distanceHistogram.size(); i++) {
        histogramIndex += distanceHistogram[i];

	if (histogramIndex >= edIndex) {
            effectiveDiameter = i;
            break;
        }
    }

    cout << "Effective diameter: " << effectiveDiameter << endl;
}
