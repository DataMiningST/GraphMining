'''
Probabilistic counter from Flajolet and Martin.
It ignores duplicates while counting the contents of a multiset.

See http://www.sciencedirect.com/science/article/pii/0022000085900418
'''

import sys

class FMCounter:
    phi = 0.77351 # Magic constant from paper

    '''
    Creates a new probabilistic counter with ncounters bitvectors and a maximum word size of wordsize.
    The wordsize is not checked later on, passing hashes wider than wordsize leads to undefined behaviour.
    '''
    def __init__(self, ncounters, wordsize):
        self.counters = [0] * ncounters
        self.wordsize = wordsize

    '''
    Adds the hash h to the counter.
    If the values for h are not uniformly randomly distributed, they should be hashed before.
    '''
    def add(self, h):
        i = h % len(counters)
        bit = smallestOneBit(h // len(counters))
        self.counters[i] |= bit
    
    '''
    Returns an integer that has only the smallest one bit of n set.
    '''
    def smallestOneBit(self, n):
        if n == 0:
            return 2**wordsize
    
        result = 1
        
        while n & result == 0:
            result *= 2
        
        return result
    
    '''
    Returns the position of the smallest zero bit in n.
    '''
    def smallestZeroBitPosition(self, n):
        result = 0
        
        while n & 1 == 1:
            result += 1
            n //= 2
        
        return result
    
    def evaluate(self):
        sum = 0
    
        for counter in counters:
            sum += smallestZeroBitPosition(counter)
        
        return int(len(counters) / phi * 2**(sum / len(counters)))
