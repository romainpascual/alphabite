import operator as op
from functools import reduce

class Misc (object):

    def __init__(self):
        self.comb_hash = dict()
        self.binom_hash = dict()
    
    def comb(self, n, k):
        k = min(k, n-k)
        if (n,k) not in self.comb_hash.keys():
            numer = reduce(op.mul, range(n, n-k, -1), 1)
            denom = reduce(op.mul, range(1, k+1), 1)
            self.comb_hash[(n,k)] = numer // denom
        return self.comb_hash[(n,k)]
            

    def p_binom(self, n, k, p):
        if (n,k,p) not in self.binom_hash.keys():
            self.binom_hash[(n,k,p)] = self.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
        return self.binom_hash[(n,k,p)]
