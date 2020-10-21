import numpy as np
from itertools import product
import utilities as U

def fill_square(n, forward=True):
    sqr = np.arange(n**2) + 1
    if not forward:
        sqr = sqr[::-1]
    return sqr.reshape((n, n))

# The other version of this code is better
# def get_submask_indices(row_range, col_range):
    # https://stackoverflow.com/a/49805163
    # Here row_range and col_range are after doing the np.arange
    # return tuple(np.transpose(list(product(row_range, col_range))))

def get_submask_indices(row_low, row_high, col_low, col_high):
    # https://stackoverflow.com/a/41900850
    rows, cols = zip(*product(np.arange(row_low, row_high),
                        np.arange(col_low, col_high)))
    return rows, cols

def make_mask(n):
    U.assert_divisibility(n, 4)
    k = U.get_k(n)
    s = np.zeros((n, n))

    # top left: i<k, j <k
    s[get_submask_indices(0, k, 0, k)] = 1
    # top right: i<k, j>3k
    s[get_submask_indices(0, k, 3*k, n)] = 1
    # bottom left: i>3k, j<k
    s[get_submask_indices(3*k, n, 0, k)] = 1
    # Bottom right: i > 3k, j > 3k
    s[get_submask_indices(3*k, n, 3*k, n)] = 1
    # Middle square
    s[get_submask_indices(k, 3*k, k, 3*k)] = 1

    return s

def construct_doubly_even_magic_square(n):
    '''
    This method was picked from the following WikiHow page on October 17, 2020.

    https://www.wikihow.com/Solve-a-Magic-Square#Solving-a-Doubly-Even-Magic-Square
    '''
    U.assert_divisibility(n, 4)
    # To fill counting forward
    s_forward = fill_square(n)
    # To fill counting backwards
    s_backward = fill_square(n, forward=False)
    # To decide when to fill forward and when backwards
    mask = make_mask(n)
    magic_s = np.zeros((n, n), dtype=int)
    # The actual filling in according to the masking
    magic_s = np.where(mask, s_forward, s_backward)
    return magic_s

n = 8
print("\nFor an {:d} x {:d} magic square, the required sum is: {:d}\n".format(n, n, U.calculate_required_sum(n)))
magic_s = construct_doubly_even_magic_square(n)
U.set_better_np_printoptions(n)
print(magic_s)
U.verify_magic_square(magic_s)
