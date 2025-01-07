'''Tools.'''


from numba import float32, int64, jit
import numpy as np


def make_mean_over_largest(k):
    def mean_over_largest(vector):
        return mean_over_k_nonzero_largest(vector, k = int(k))

    return mean_over_largest


def make_mean_over_consecutive_largest(k):
    def mean_over_consecutive_largest(vector):
        return mean_over_k_consecutive_largest(vector, k = int(k))

    return mean_over_consecutive_largest


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


@jit(float32(float32[:], int64), nopython=True)
def mean_over_k_consecutive_largest(vector, k):
    '''Return the mean over the k largest consecutive values of a vector.'''
    if k == 0:
        return 0
    nonzeros = (vector > 0.0).sum()
    if k >= nonzeros:
        return vector.sum() / (nonzeros + (nonzeros == 0))

    if k == 1:
        return vector.max()

    n = len(vector)
    mean = np.zeros(n + 1 - k, dtype = np.float32)
    for p in range(n + 1 - k):
        for i in range(k):
            mean[p] += vector[p + i]
        mean[p] = mean[p] / k
    return mean.max()
