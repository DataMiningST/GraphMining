'''
Probabilistic counter from Flajolet and Martin.

The counter can either be used to ignore duplicates while counting the contents of a multiset,
or to count the size of set unions.
If the counter is used to count the size of set unions, it must be initialized with the initialize method.


See http://www.sciencedirect.com/science/article/pii/0022000085900418
'''

import sys
import random
from copy import copy

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
    Copies this object.
    '''
    def copy(self):
        other = FMCounter(len(self.counters), self.wordsize)
        other.counters = copy(self.counters)
        return other

    '''
    Adds the hash h to the counter.
    If the values for h are not uniformly randomly distributed, they should be hashed before.
    '''
    def add(self, h):
        i = h % len(self.counters)
        bit = smallestOneBit(h // len(self.counters))
        self.counters[i] |= bit
    
    '''
    Initializes the counter with a random bit.
    '''
    def initialize(self):
        for i in xrange(len(self.counters)):
            self.counters[i] = self.getFMRandomBit()
    
    '''
    Returns an integer that has only the smallest one bit of n set.
    '''
    def smallestOneBit(self, n):
        if n == 0:
            return 2**self.wordsize
    
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
    
    '''
    Evaluates the size of the counter.
    isSetUnionMode: True if the counter was used with the union method, false if it was used with the add method.
    '''
    def evaluate(self, isSetUnionMode = True):
        sum = 0.0
    
        for counter in self.counters:
            sum += self.smallestZeroBitPosition(counter)
        
        modeFactor = 1 if isSetUnionMode else len(self.counters)
        return int(modeFactor / self.phi * 2**(sum / len(self.counters)))

    def getFMRandomBit(self):
        bit = 1
        
        for i in xrange(1, self.wordsize):
            if random.getrandbits(1) == 1:
                break
            
            bit *= 2
            
        return bit
    
    def union(self, other):
        for i in xrange(self.wordsize):
            self.counters[i] |= other.counters[i]
            
    def __str__(self):
        result = ""
        
        for counter in self.counters:
            result += "|" + str(bin(counter))[2:].zfill(16)
            
        return result
