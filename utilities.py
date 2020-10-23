import numpy as np
from itertools import product
import curses
from functools import partial

def is_divisible(n, d):
    return n%d == 0

def assert_divisibility(n, d, check_indivisibility=False):
    assert is_divisible(n, d), "Divisibility of {:d} by {:d} failed".format(n, d)
    return True

def assert_indivisibility(n, d):
    assert not is_divisible(n, d), "{:d} should not be divisible by {:d} failed".format(n, d)
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

def get_display_size(n):
    return int(np.ceil(np.log10(n**2)))+1

def get_display_format_string(n):
    return "{:"+str(get_display_size(n))+"d}"

def np_int_formatter(n, x):
    if x == 0:
        return " "*(get_display_size(n)-1)+"_"
    else:
        return get_display_format_string(n).format(x)

def set_better_np_printoptions(n):
    display_size = get_display_size(n)
    display_format_string = get_display_format_string(n)
    formatter = partial(np_int_formatter, n)
    np.set_printoptions(formatter={"int": formatter})

def verify_magic_square(magic_s, print_message=True, print_verbose=False):
    n = magic_s.shape[0]
    assert n==magic_s.shape[1], "Input is not a square"
    required_sum = calculate_required_sum(n)
    print_message = print_message or print_verbose
    magic_flag = True           # boolean keeping track of magicness
    if print_message:
        print("\n"+"-"*40)
        print("Starting verification:\nSquare size: {:d}x{:d}\nRequired sum: {:d}".format(n, n, required_sum))
        print("-"*20)

    # columns
    cols = np.sum(magic_s, 0)
    # Doesn't add up!
    if np.any(cols != required_sum):
        magic_flag = False
        print("{:d} columns don't add up to required sum".format(np.count_nonzero(cols != required_sum)))
        if print_verbose:
            for col in np.argwhere(cols != required_sum).flatten():
                faulty_column = magic_s[:, col].flatten()
                print("Column {}: {} adds upto {:d}".format(col+1, faulty_column, np.sum(faulty_column)))
    elif print_verbose:
        print("Yes. All columns add up to {:d}".format(required_sum))

    # rows
    rows = np.sum(magic_s, 1)
    if np.any(rows != required_sum):
        magic_flag = False
        print("{:d} rows don't add up to required sum".format(np.count_nonzero(rows != required_sum)))
        if print_verbose:
            for row in np.argwhere(rows != required_sum).flatten():
                faulty_row = magic_s[row, :].flatten()
                print("Column {}: {} adds upto {:d}".format(row+1, faulty_row, np.sum(faulty_row)))
    elif print_verbose:
        print("Yes. All rows add up to {:d}".format(required_sum))

    # main diagonal (top left to bottom right)
    diagonal_1_sum = np.trace(magic_s)
    if diagonal_1_sum != required_sum:
        magic_flag = False
        faulty_diagonal = magic_s[np.arange(n), np.arange(n)]
        print("The main diagonal: {} adds upto {:d}".format(faulty_diagonal, diagonal_1_sum))
    elif print_verbose:
        print("Yes. The main diagonal adds up to {:d}".format(required_sum))

    # other diagonal (bottom left to top right)
    diagonal_2_sum = np.trace(np.rot90(magic_s))
    if diagonal_2_sum != required_sum:
        magic_flag = False
        faulty_diagonal = magic_s[np.arange(n)[::-1], np.arange(n)]
        print("The other diagonal {} adds upto {:d}".format(faulty_diagonal, diagonal_2_sum))
    elif print_verbose:
        print("Yes. The other diagonal also adds up to {:d}".format(required_sum))

    # Final printing if all work out
    if print_message:
        if magic_flag:
            print("Finished checking. All rows, columns and diagonals add up to {:d}.\nSquare is indeed magic!".format(required_sum))
        else:
            print("Finished checking. Some rows/columns/diagonals do NOT add up to {:d}.\nSquare is NOT magic!".format(required_sum))
        print("-"*40)

    return magic_flag
