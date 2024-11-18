'''Tools.'''


from numba import float32, int64, jit
import numpy as np


def make_mean_over_largest(k):
    def mean_over_largest(vector):
        return mean_over_k_nonzero_largest(vector, k = int(k))

    return mean_over_largest


@jit(float32(float32[:], int64), nopython=True)
def mean_over_k_nonzero_largest(vector, k):
    '''Return the mean over the k largest values of a vector.'''
    if k == 0:
        return 0
    nonzeros = (vector > 0.0).sum()
    if k >= nonzeros:
        return vector.sum() / (nonzeros + (nonzeros == 0))

    z = -np.partition(-vector, kth = k)
    upper_bound = min(k, nonzeros)
    return z[:upper_bound].sum() / upper_bound
