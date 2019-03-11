import operator as op
from functools import reduce

comb_hash = {}
p_binom_hash = {}


def comb(n, k):  # Computes n choose k
    hash_string = "{0}:{1}".format(n, k)
    if not hasattr(comb_hash, hash_string):
        k = min(k, n-k)
        numer = reduce(op.mul, range(n, n-k, -1), 1)
        denom = reduce(op.mul, range(1, k+1), 1)
        comb_hash[hash_string] = numer / denom
    return comb_hash[hash_string]


def p_binom(n, k, p):
    hash_string = "{0}:{1}:{2}".format(n, k, p)
    if not hasattr(p_binom_hash, hash_string):
        p_binom_hash[hash_string] = comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    return p_binom_hash[hash_string]
