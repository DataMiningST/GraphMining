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

#include "FMCounter.h"

#include <cmath>


inline uint8_t FMCounter::smallestZeroBitPosition(uint32_t n) {
    uint8_t result = 0;

    while ((n & 1) == 1) {
        result++;
        n >>= 1;
    }

    return result;
}

inline uint32_t FMCounter::getFMRandomBit(mt19937& random) {
    uint32_t result = 1;

    for (int i = 0; i < 31; i++) {
	if (__builtin_popcount(random()) & 1) {
            break;
	}

	result <<= 1;
    }

    return result;
}

FMCounter::FMCounter(int ncounters) : ncounters(ncounters) {
}

void FMCounter::initialize(mt19937& random, uint32_t *counters) {
    for (int i = 0; i < ncounters; i++) {
	    counters[i] = getFMRandomBit(random);
    }
}

uint64_t FMCounter::evaluate(uint32_t *counters) {
    double sum = 0;

    for (int i = 0; i < ncounters; i++) {
	    sum += smallestZeroBitPosition(counters[i]);
    }

    return (uint64_t) (1.0 / phi * pow(2, sum / ncounters));
}

void FMCounter::_union(uint32_t *selfCounters, uint32_t *otherCounters) {
    for (int i = 0; i < ncounters; i++) {
	    selfCounters[i] |= otherCounters[i];
    }
}
