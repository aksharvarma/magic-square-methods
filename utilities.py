import numpy as np
from itertools import product

def is_divisible(n, d):
    return n%d == 0

def assert_divisibility(n, d, check_indivisibility=False):
    assert is_divisible(n, d), "Divisibility of {:d} by {:d} failed".format(n, d)
    return True

def assert_indivisibility(n, d):
    assert not is_divisible(n, d), "Divisibility of {:d} by {:d} failed".format(n, d)
    return True

def calculate_required_sum(n):
    return n*(n**2 + 1)//2

def get_k(n):
    if is_divisible(n, 4):
        return n//4
    elif is_divisible(n, 2):
        return (n-2)//4
    else:
        return (n-1)//2

def set_better_np_printoptions(n):
    display_size = str(int(np.ceil(np.log10(n**2)))+1)
    display_string = "{:"+display_size+"d}"
    np.set_printoptions(formatter={"int": lambda x: display_string.format(x)})

def verify_magic_square(magic_s, print_message=True, print_verbose=False):
    n = magic_s.shape[0]
    assert n==magic_s.shape[1], "Input is not a square"
    required_sum = calculate_required_sum(n)
    print_message = print_message or print_verbose
    if print_message:
        print("\nStarting to verify if the required sum of {:d} is attained.".format(required_sum))
    # columns
    cols = np.sum(magic_s, 0)
    assert np.all(cols == required_sum)
    if print_verbose:
        print("Yes. All columns add up to {:d}".format(required_sum))
    # rows
    rows = np.sum(magic_s, 1)
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
