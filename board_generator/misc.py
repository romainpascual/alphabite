import operator as op
from functools import reduce


def comb(n, k):  # Computes n choose k
    k = min(k, n-k)
    numer = reduce(op.mul, range(n, n-k, -1), 1)
    denom = reduce(op.mul, range(1, k+1), 1)
    return numer / denom
