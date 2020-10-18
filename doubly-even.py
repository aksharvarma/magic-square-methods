import numpy as np
from itertools import product

def assert_divisibility(n, d):
    assert n%d == 0, "Divisibility of {:d} by {:d} failed".format(n, d)

def fill_square(n, forward=True):
    sqr = np.arange(n**2) + 1
    if not forward:
        sqr = sqr[::-1]
    return sqr.reshape((n, n))

# def get_indices(row_range, col_range):
    # https://stackoverflow.com/a/49805163
    # Here row_range and col_range are after doing the np.arange
    # return tuple(np.transpose(list(product(row_range, col_range))))

def get_indices(row_low, row_high, col_low, col_high):
    # https://stackoverflow.com/a/41900850
    rows, cols = zip(*product(np.arange(row_low, row_high),
                        np.arange(col_low, col_high)))
    return rows, cols

def make_mask(n):
    assert_divisibility(n, 4)
    k = n//4
    s = np.zeros((n, n))

    # top left: i<k, j <k
    s[get_indices(0, k, 0, k)] = 1
    # top right: i<k, j>3k
    s[get_indices(0, k, 3*k, n)] = 1
    # bottom left: i>3k, j<k
    s[get_indices(3*k, n, 0, k)] = 1
    # Bottom right: i > 3k, j > 3k
    s[get_indices(3*k, n, 3*k, n)] = 1
    # Middle square
    s[get_indices(k, 3*k, k, 3*k)] = 1

    return s

def magic_square(n):
    assert_divisibility(n, 4)
    s_forward = fill_square(n)
    s_backward = fill_square(n, forward=False)
    mask = make_mask(n)
    magic_s = np.zeros((n, n))
    magic_s = np.where(mask, s_forward, s_backward)
    return magic_s

def calculate_required_sum(n):
    return n*(n**2 + 1)//2

def verify_magic(s, print_message=True, print_verbose=False):
    n = s.shape[0]
    assert n==s.shape[1], "Input is not a square"
    assert_divisibility(n, 4)
    required_sum = calculate_required_sum(n)
    print_message = print_message or print_verbose
    if print_message:
        print("\nStarting to verify if the required sum of {:d} is attained.".format(required_sum))
    # columns
    cols = np.sum(s, 0)
    assert np.all(cols == required_sum)
    if print_verbose:
        print("Yes. All columns add up to {:d}".format(required_sum))
    # rows
    rows = np.sum(s, 1)
    assert np.all(rows == required_sum)
    if print_verbose:
        print("Yes. All rows add up to {:d}".format(required_sum))
    # main diagonal (top left to bottom right)
    diagonal_1 = np.trace(magic_s)
    assert diagonal_1 == required_sum
    if print_verbose:
        print("Yes. The main diagonal adds up to {:d}".format(required_sum))
    # other diagonal (bottom left to top right)
    diagonal_2 = np.trace(np.rot90(magic_s))
    assert diagonal_2 == required_sum
    if print_verbose:
        print("Yes. The other diagonal also adds up to {:d}".format(required_sum))
    # assert cols == rows == diagonal_1 == diagonal_2 == required_sum
    if print_message:
        print("Done. All rows, columns and diagonals add up to {:d}.\nSquare is indeed magic.".format(required_sum))
    return True

n = 16
k = n//4
s_forward = fill_square(n)
s_backward = fill_square(n, False)
# print(sqr_forward)
# print(sqr_backward)
mask = make_mask(n)
# print(mask)
magic_s = np.where(mask, s_forward, s_backward)
print("\nThe required sum is: {:d}\n".format(calculate_required_sum(n)))
print(magic_s)
verify_magic(magic_s, print_message=True, print_verbose=False)
