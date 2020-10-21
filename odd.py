import numpy as np
from itertools import product
import utilities as U

def construct_odd_magic_square(n):
    '''
    This follows the Siamese method, which isn't the best for a computer,
    but is very easy for a human for follow. This function allows comparing
    a human constructed magic square to one a computer generates and verifies.

    Reference: https://en.wikipedia.org/wiki/Siamese_method
    '''
    U.assert_indivisibility(n, 2)
    magic_s = np.zeros((n, n), dtype=int)
    # Start from 1
    current_num = 1
    # First cell to fill is the middle one on the top row.
    i, j = 0, U.get_k(n)
    while current_num <= n**2:
        magic_s[i, j] = current_num
        # Move up and right
        new_i, new_j = (i-1)%n, (j+1)%n
        if magic_s[new_i, new_j] != 0:
            # If that is already filled, drop down instead.
            new_i, new_j = i+1, j
        i, j = new_i, new_j
        current_num +=1         # Will now fill in the next number

    return magic_s

n = 5
print("\nFor an {:d} x {:d} magic square, the required sum is: {:d}\n".format(n, n, U.calculate_required_sum(n)))
magic_s = construct_odd_magic_square(n)
U.set_better_np_printoptions(n)
print(magic_s)
U.verify_magic_square(magic_s)
