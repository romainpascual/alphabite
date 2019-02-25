# -*- coding: utf-8 -*-

# @class Board

# -- Third-party modules

##
# @brief A tool for board simulation
#

class Board( object ):
    
    # ----------------------------------------------------------------------------
    # -- CLASS ATTRIBUTES
    # ----------------------------------------------------------------------------

    # Error status
    SUCCESS = 0
    FAILURE = 1

    # ----------------------------------------------------------------------------
    # -- INITIALIZATION
    # ----------------------------------------------------------------------------

    def __init__(
            self,
            n=0,
            m=0):

        # -- Errors
        self.__err_code = Board.FAILURE
        self.__err_msg = "Board.init()"
    
        # Attributs
        self.__n = n
        self.__m = m
        self.__mat = [[None for _ in range(self.__m)] for _ in range(self.__n)]
        self.__species = None

        # -- Errors
        self.__err_code = Board.SUCCESS
        self.__err_msg = ""

    # END def __init__

    @staticmethod
    def create_from_board(previous_board, cell_list):
        """
        Create a new board from a previous board and a given cell list to change
        """
        new_board = Board(previous_board.height(), previous_board.width())
        new_board.__mat = previous_board.__mat
        for cell in cell_list:
            new_board.__mat[cell.get_x(), cell.get_y()] = cell
        return new_board
    
    # END create_from_board

    # ----------------------------------------------------------------------------
    # -- GETTERS AND SETTERS
    # ----------------------------------------------------------------------------

    def build(self, n , m):
        """
        Build the board with the given sizes.
        Can be used to reset the map.
        """
        self.__init__(n,m)

    def width(self):
        """
        Get width
        """
        return self.__m
    
    # END width

    def height(self):
        """
        Get height
        """
        return self.__n
    
    # END height

    def getCell(self, i, j):
        """
        Return the content of the cell at position(i,j)
        """
        return self.__mat[i,j]

    # END getCell

    # ----------------------------------------------------------------------------
    # -- UPDATE
    # ----------------------------------------------------------------------------

    def update(self, upd):
        """
        update the board according to upd=[(x, y, cell)]
        """
        # -- Errors
        self.__err_code = Board.FAILURE
        self.__err_msg = "Board.update()"

        for up in upd:
            self.__mat[up[0], up[1]] = up[[2]]

        # -- Errors
        self.__err_code = Board.SUCCESS
        self.__err_msg = ""

    # END update

    def set_species(self, x, y):
        """
        Using the home cell, find out which species we are
        """
        self.__species = self.__mat[x,y].get_species()
    
    # END set_species

    def get_species(self):
        """
        Return our species
        """
        return self.__species
    
    # END get_species