# -*- coding: utf-8 -*-

# -- Standard modules
import sys
import time

# -- MRG modules
from board import Board

# -- Constants

# Error
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Program description
PROG_NAME = "[boardTest]"
MIN_ARGC = 1
HELP = """
  BRIEF: Tests call Board.
  ARGS:
        [-h] # Displays this description.
"""

# -- main ----------------------------------------------------------------------
def main ( argv=[PROG_NAME] ) :

  # ----------------------------------------------------------------------------
  # -- INITIALIZATION
  # ----------------------------------------------------------------------------

  # board handler
  board = Board()

  # board size
  n = 10
  m = 5

  # initial board
  upd = [(9, 0, (2, 'h')), (4, 1, (4, 'w')), (2, 2, (4, 'h')), (9, 2, (1, 'h')), (4, 3, (4, 'v')), (9, 4, (2, 'h'))]
  
  # ----------------------------------------------------------------------------
  # -- ARGUMENTS
  # ----------------------------------------------------------------------------

  # -- check minimum number of arguments
  argc = len(argv)
  if (argc < MIN_ARGC) :
    print(HELP)
    return EXIT_FAILURE

  # -- print help (-h)
  if ("-h" in argv[MIN_ARGC:]) :
    print(HELP)
    return EXIT_SUCCESS

  