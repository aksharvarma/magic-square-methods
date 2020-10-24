# Replicating Pen and Paper Magic Squares methods

This repo implements various pen and paper methods that can be used by a human to fill in an _n x n_ square with numbers from 1 to _n*n_ such that each row, column and the two diagonals all add up to the same sum.

Included in this repo are three files which implement three different methods of making _n x n_ magic squares with different divisibility properties. The goal is not to have a quick algorithm, but to replicate a simple method that a human with a pen and paper could perform. The focus is on using a method that does not require rewriting/erasing already filled in values. This repo implements those methods so that checking one's work can be delegated to a machine. 

tl;dr - I coded this up mainly because I was lazy to add up some numbers in the squares that I filled in.

## Odd n
The simplest cases for humans are when the size _n_ of the square is an odd number. These use the [Siamese method](https://en.wikipedia.org/wiki/Siamese_method).

## Doubly Even n
When _n_ is divisible by 4, it is called doubly even and these are also simple to solve. This uses a method of making a mask on the square and filling numbers counting forward in the mask and numbers counting backwards outside the mask. The method is explained better on this [Wikihow page](https://www.wikihow.com/Solve-a-Magic-Square#Solving-a-Doubly-Even-Magic-Square).

## Singly Even n
When _n_ is divisible by 2 but not by 4, it is called the singly even case. This is the hardest for a human to solve and is based on the Siamese method for odd numbers. The method is [Conway's LUX method](https://en.wikipedia.org/wiki/Conway%27s_LUX_method_for_magic_squares).


# Running and Organization

This code should work with Python 3+. The primary libraries used are `numpy`, `itertools`, and `enum`. 

Each type of method is implemented in its own file. You can simply change the value of _n_ in the code and get a magic square of size _n x n_. If you want a self-contained function that will do everything for you, then there is the `MagicSquare` class in the `magic_square.py` file which you can use. A short example code to use that is available in `run_magic_square.py` which illustrates the main functionality.

There is also a `utilities.py` file which contains various functions that are used in each of the methods, including the code that verifies that the squares constructed are indeed magic squares.

## Curses

Currently, the `odd.py` file contains some code that allows a crude step-by-step visualization of the method for Siamese method used for odd _n_. This utilizes some helper functions inside `curses_utilities.py`. To run the code in this manner simply use `python odd.py n use_curses` substituting the odd number _n_ that you wish to see the visualization for.

The code is currently slightly hacky, but there are plans to clean it up, integrate it into the modular class code in `magic_square.py` and expand out the functionality.
