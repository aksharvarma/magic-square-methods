import numpy as np
from itertools import product
from enum import Enum
import utilities as U

class Evenness(Enum):
    Odd = 1
    SinglyEven = 2
    DoublyEven = 4

    def __repr__(self):
        return self.name

class MagicSquare:
    def __init__(self, n=None, verbose=False):
        if n is None:
            print("Setting n to default of 3")
            n = 3
        self.n = n
        self.verbose=verbose
        self._set_values()

    def _set_values(self):
        n = self.n
        self.required_sum = U.calculate_required_sum(n)
        self.evenness = self.set_evenness()
        self.magic_s = None
        self.choices = {Evenness.DoublyEven: self._construct_doubly_even,
                        Evenness.SinglyEven: self._construct_singly_even,
                        Evenness.Odd: self._construct_odd}
        U.set_better_np_printoptions(n)

    def set_evenness(self):
        n = self.n
        if U.is_divisible(n, 4):
            return Evenness.DoublyEven
        elif U.is_divisible(n, 2):
            return Evenness.SinglyEven
        else:
            return Evenness.Odd

    def run(self):
        n = self.n
        print("\nFor an {:d} x {:d} magic square, the required sum is: {:d}\n".format(n, n, self.required_sum))
        magic_s = self.construct()
        print(magic_s)
        self.verify()

    def construct(self):
        self.magic_s = self.choices[self.evenness]()
        return self.magic_s

    def get_magic_s(self):
        if self.magic_s is None:
            self.construct()
        return self.magic_s

    def set_magic_s(self, magic_s):
        self.magic_s = magic_s

    def verify(self, magic_s=None,
               print_square=False, print_message=True, print_verbose=None):
        if magic_s is None:
            magic_s=self.get_magic_s()
        if print_square:
            print("\nWe'll now verify the following square:")
            print(magic_s)
        print_verbose = self.verbose if print_verbose is None else print_verbose
        return U.verify_magic_square(magic_s,
                                     print_message=print_message,
                                     print_verbose=print_verbose)

    # The functions below are lifted from their individual files
    # The individual files are better if you want to understand what
    # each internal function does, and just to play around with.
    # This class if more in case someone wants the final working set.
    def _construct_odd(self):
        '''
        This follows the Siamese method, which isn't the best for a computer,
        but is very easy for a human for follow. This function allows comparing
        a human constructed magic square to one a computer generates and verifies.

        Reference: https://en.wikipedia.org/wiki/Siamese_method
        '''
        n = self.n
        U.assert_indivisibility(n, 2)
        magic_s = np.full((n, n), U.EMPTY_CELL, dtype=int)
        # Start from 1
        current_num = 1
        # First cell to fill is the middle one on the top row.
        i, j = 0, U.get_k(n)
        while current_num <= n**2:
            magic_s[i, j] = current_num
            # Move up and right
            new_i, new_j = (i-1)%n, (j+1)%n
            if magic_s[new_i, new_j] != U.EMPTY_CELL:
                # If that is already filled, drop down instead.
                new_i, new_j = i+1, j
            i, j = new_i, new_j
            current_num +=1         # Will now fill in the next number

        return magic_s

    def _construct_doubly_even(self):
        '''
        This method was picked from the following WikiHow page on October 17, 2020.

        https://www.wikihow.com/Solve-a-Magic-Square#Solving-a-Doubly-Even-Magic-Square
        '''
        n = self.n

        def fill_square(n, forward=True):
            sqr = np.arange(n**2) + 1
            if not forward:
                sqr = sqr[::-1]
            return sqr.reshape((n, n))

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

        # To fill counting forward
        s_forward = fill_square(n)
        # To fill counting backwards
        s_backward = fill_square(n, forward=False)
        # To decide when to fill forward and when backwards
        mask = make_mask(n)
        self.magic_s = np.zeros((n, n), dtype=int)
        # The actual filling in according to the masking
        self.magic_s = np.where(mask, s_forward, s_backward)
        return self.magic_s

    def _construct_singly_even(self):
        '''
        This uses Conway's LUX method, which may not be the best for a computer,
        but is very easy for a human for follow. Hence this allows comparing
        a human constructed magic square to one a computer generates and verifies.

        Reference: https://en.wikipedia.org/wiki/Conway%27s_LUX_method_for_magic_squares
        '''
        n = self.n

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

        self.magic_s = np.full((n, n), U.EMPTY_CELL, dtype=np.int)
        k = U.get_k(n)
        LUX = make_LUX_square(k)

        if self.verbose:
            print("The LUX square constructed is as follows:\n", LUX, "\n")

        LUX_size = LUX.shape[0]
        # Start from 1
        current_block = np.arange(4) + 1
        # First cell to fill is the middle one on the top row.
        i, j = 0, (LUX_size-1)//2
        while current_block[-1] <= n**2:
            fill_block(self.magic_s, current_block, i, j, LUX[i, j])
            # magic_s[i, j] = current_num
            # Move up and right
            new_i, new_j = (i-1) % LUX_size, (j+1) % LUX_size
            if self.magic_s[2*new_i, 2*new_j] != U.EMPTY_CELL:
                # If that is already filled, drop down instead.
                new_i, new_j = i+1, j
            i, j = new_i, new_j
            current_block = current_block + 4         # To fill next block

        return self.magic_s
