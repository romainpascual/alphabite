import operator as op
from functools import reduce

class Misc (object):

    comb_hash = dict()
    binom_hash = dict()

    @staticmethod
    def comb(n, k):
        k = min(k, n-k)
        if (n,k) not in Misc.comb_hash.keys():
            numer = reduce(op.mul, range(n, n-k, -1), 1)
            denom = reduce(op.mul, range(1, k+1), 1)
            Misc.comb_hash[(n,k)] = numer // denom
        return Misc.comb_hash[(n,k)]

    @staticmethod
    def p_binom(n, k, p):
        if (n,k,p) not in Misc.binom_hash.keys():
            Misc.binom_hash[(n,k,p)] = Misc.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
        return Misc.binom_hash[(n,k,p)]
