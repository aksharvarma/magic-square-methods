import numpy as np
from itertools import product
import utilities as U
import curses
import curses_utilities as CU
import traceback
import sys

def construct_odd_magic_square(n, w=None, base_yx=None, delay=500):
    '''
    This follows the Siamese method, which isn't the best for a computer,
    but is very easy for a human for follow. This function allows comparing
    a human constructed magic square to one a computer generates and verifies.

    Reference: https://en.wikipedia.org/wiki/Siamese_method
    '''
    U.assert_indivisibility(n, 2)
    magic_s = np.full((n, n), U.EMPTY_CELL, dtype=int)
    if w is not None:           # If using curses for displaying updates
        w.addstr(*base_yx, "{}".format(magic_s))
        w.refresh()
        CU.pause_for(delay)
    # Start from 1
    current_num = 1
    # First cell to fill is the middle one on the top row.
    i, j = 0, U.get_k(n)
    while current_num <= n**2:
        magic_s[i, j] = current_num
        if w is not None:       # If using curses for displaying updates
            CU.print_cell(w, magic_s, i, j, base_yx=base_yx)
        # Move up and right
        new_i, new_j = (i-1)%n, (j+1)%n
        if magic_s[new_i, new_j] != U.EMPTY_CELL:
            # If that is already filled, drop down instead.
            new_i, new_j = (i+1)%n, j%n
        i, j = new_i, new_j
        current_num +=1         # Will now fill in the next number

    return magic_s

n = 5
use_curses = False
if len(sys.argv) > 2 and sys.argv[2]=="use_curses":
    n, use_curses = int(sys.argv[1]), True
elif len(sys.argv) > 1:
    n = int(sys.argv[1])

print("\nFor an {:d} x {:d} magic square, the required sum is: {:d}\n".format(n, n, U.calculate_required_sum(n)))
U.set_better_np_printoptions(n)

if use_curses:
    try:
        w = CU.curses_init()
        w.addstr("\nFor an {:d} x {:d} magic square, the required sum is: {:d}\n".format(n, n, U.calculate_required_sum(n)))
        w.refresh()
        CU.pause_for(500)
        y, x = w.getyx()
        magic_s = construct_odd_magic_square(n, w, base_yx=(y+2, 0))
        y, x = w.getyx()
        CU.pause_for(1000)
        w.addstr(y+2, 0, "Press any key to continue...")
        w.refresh()
        w.getch()
        exception = None
    except:
        print("Throwing an error now!!")
        exception = traceback.format_exc()     # print trace back log of the error
    finally:
        print("Closing curses...")
        CU.curses_close(w)
    if exception is not None:
        print("Exception occured!")
        print(exception)
        print("Continuing after that...")
else:
    magic_s = construct_odd_magic_square(n)

print(magic_s)
U.verify_magic_square(magic_s)
