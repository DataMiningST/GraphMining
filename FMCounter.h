/*
 * Probabilistic counter from Flajolet and Martin.
 *
 * The counter can either be used to ignore duplicates while counting the contents of a multiset,
 * or to count the size of set unions.
 * If the counter is used to count the size of set unions, it must be initialized with the initialize method.
 *
 *
 * See http://www.sciencedirect.com/science/article/pii/0022000085900418
 */

#include <random>

const int ncounters = 64; // Value used in paper, gives average error < 10%

using namespace std;

class FMCounter {
private:
    int ncounters;
    static constexpr double phi = 0.77351; // Magic constant from paper

    // Calculates the position of the smallest zero bit in n
    uint8_t smallestZeroBitPosition(uint32_t n);

    uint32_t getFMRandomBit(mt19937& random);
    
public:
    FMCounter(int ncounters);

    void initialize(mt19937& random, uint32_t *counters);

    // Evaluates the size of the counter
    uint64_t evaluate(uint32_t *counters);

    void _union(uint32_t *selfCounters, uint32_t *otherCounters);
};
