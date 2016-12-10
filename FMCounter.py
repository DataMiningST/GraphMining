'''
Probabilistic counter from Flajolet and Martin.

See http://www.sciencedirect.com/science/article/pii/0022000085900418
'''

class FMCounter:
    def __init__(self, ncounters):
        self.counters = [0] * ncounters

    def add(self, object):
        h = hash(object) # BAD HASH FUNCTION!!!
        
        i = h % len(counters)
        bit = smallestOneBit(h // len(counters))
    
    def smallestOneBit(self, n):
            
