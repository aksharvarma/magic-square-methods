import numpy as np
from itertools import product
import utilities as U
from enum import Enum

class Block(Enum):
    L = -1
    U = 0
    X = 1

    def __repr__(self):
        return self.name

def make_LUX_square(k):
    # assert_indivisibility(odd_num, 2)
    LUX = np.zeros((2*k+1, 2*k+1), dtype=Block)
    # Fill first n+1 with L
    LUX[:k+1, :] = Block.L
    # Fill next with U
    LUX[k+1, :] = Block.U
    # Fill remaining n-1 with X
    LUX[k+2:, :] = Block.X
    # Swap middle U with the L above it.
    LUX[k, k] = Block.U
    LUX[k+1, k] = Block.L
    return LUX

def fill_block(magic_s, block, i, j, LUX_type=None):
    assert LUX_type is not None, "LUX_type not provided"
    if LUX_type is Block.L:       # Fill in L
        magic_s[2*i, 2*j+1] = block[0]
        magic_s[2*i+1, 2*j] = block[1]
        magic_s[2*i+1, 2*j+1] = block[2]
        magic_s[2*i, 2*j] = block[3]
    if LUX_type is Block.U:       # Fill in U
        magic_s[2*i, 2*j] = block[0]
        magic_s[2*i+1, 2*j] = block[1]
        magic_s[2*i+1, 2*j+1] = block[2]
        magic_s[2*i, 2*j+1] = block[3]
    if LUX_type is Block.X:       # Fill in X
        magic_s[2*i, 2*j] = block[0]
        magic_s[2*i+1, 2*j+1] = block[1]
        magic_s[2*i+1, 2*j] = block[2]
        magic_s[2*i, 2*j+1] = block[3]

def construct_singly_even_magic_square(n, print_LUX=True):
    '''
    This uses Conway's LUX method, which may not be the best for a computer,
    but is very easy for a human for follow. Hence this allows comparing
    a human constructed magic square to one a computer generates and verifies.

    Reference: https://en.wikipedia.org/wiki/Conway%27s_LUX_method_for_magic_squares
    '''
    U.assert_divisibility(n, 2)
    U.assert_indivisibility(n, 4)
    magic_s = np.zeros((n, n), dtype=np.int)
    k = U.get_k(n)
    LUX = make_LUX_square(k)
    print("The LUX square constructed is as follows:\n", LUX, "\n")
    LUX_size = LUX.shape[0]
    # Start from 1
    current_block = np.arange(4) + 1
    # First cell to fill is the middle one on the top row.
    i, j = 0, (LUX_size-1)//2
    while current_block[-1] <= n**2:
        fill_block(magic_s, current_block, i, j, LUX[i, j])
        # magic_s[i, j] = current_num
        # Move up and right
        new_i, new_j = (i-1) % LUX_size, (j+1) % LUX_size
        if magic_s[2*new_i, 2*new_j] != 0:
            # If that is already filled, drop down instead.
            new_i, new_j = i+1, j
        i, j = new_i, new_j
        current_block = current_block + 4         # To fill next block

    return magic_s



n = 6
print("\nFor an {:d} x {:d} magic square, the required sum is: {:d}\n".format(n, n, U.calculate_required_sum(n)))
magic_s = construct_singly_even_magic_square(n)
U.set_better_np_printoptions(n)
print(magic_s)
U.verify_magic_square(magic_s)
