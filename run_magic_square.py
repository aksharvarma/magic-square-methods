from magic_square import MagicSquare
import numpy as np
import utilities as U

# Just some code to show how to use the MagicSquare class
for n in [10, 11, 12]:
    verbose = True if n > 11 else False    # not cluttering for all sizes n
    ms = MagicSquare(n, verbose=verbose)


    # ms.run() does the following internally
    # So you can simply call that or have more fine grained control.
    print("\nFor an {:d} x {:d} magic square, the required sum is: {:d}\n".format(n, n, ms.required_sum))
    magic_s = ms.construct()
    print(magic_s)
    ms.verify()

# You can also test a magic square you hand constructed as follows
print("Testing for a hand crafted 3x3 magic square")
my_magic_s = np.array([[8, 1, 6],
                       [3, 5, 7],
                       [4, 9, 2]])  # A 3x3 magic square
MagicSquare(3, verbose=True).verify(my_magic_s, print_square=True)

# A 4x4 non-magic square (consecutive numbers are not used for this)
print("Testing for a hand crafted 4x4 NON-magic square.")
my_non_magic_s = np.array([[8, 1, 6, 10],
                           [7, 4, 12, 11],
                           [4, 9, 2, 12],
                           [15, 14, 15, 16]])  # This is not a magic square
required_sum = U.calculate_required_sum(4)
MagicSquare(4).verify(my_non_magic_s,
                      print_message=True, print_verbose=True, print_square=True)
