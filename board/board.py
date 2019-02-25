# -*- coding: utf-8 -*-

# @class Board

# -- Third-party modules

# -- Program modules
from .cell import Cell

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
        self.__h = 0
        self.__v = 0
        self.__w = 0
        self.__mat = [[Cell(x, y, None, 0) for x in range(self.__m)] for y in range(self.__n)]

        self.__species = None
        self.__win = 0

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
            new_board.update_cell(cell)
        new_board.upd_win()
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

    @property
    def width(self):
        """
        Get width
        """
        return self.__m
    
    # END width

    @property
    def height(self):
        """
        Get height
        """
        return self.__n
    
    # END height

    def get_cell(self, pos):
        """
        Return the content of the cell at position(i,j)
        """
        return self.__mat[pos[0]][pos[1]]

    # END get_cell

    @property
    def h(self):
        """
        Get population of human
        """
        return self.__h

    # END h

    @property
    def v(self):
        """
        Get population of vampire
        """
        return self.__v

    # END v

    @property
    def w(self):
        """
        Get population of werewolves
        """
        return self.__w

    # END w

    # ----------------------------------------------------------------------------
    # -- UPDATE
    # ----------------------------------------------------------------------------

    def update(self, upd):
        """
        Update the board according to upd=[(x, y, (nb, species))]
        If nb=0, then specie=None
        """
        # -- Errors
        self.__err_code = Board.FAILURE
        self.__err_msg = "Board.update()"

        for up in upd:
            newCell = Cell(up[0], up[1], up[2][0], up[2][1])
            self.update_cell(newCell)
        
        self.upd_win()

        # -- Errors
        self.__err_code = Board.SUCCESS
        self.__err_msg = ""

    # END update

    def set_species(self, x, y):
        """
        Using the home cell, find out which species we are
        """
        self.__species = self.__mat[x][y].species
    
    # END set_species

    @property
    def species(self):
        """
        Return our species
        """
        return self.__species
    
    # END get_species

    def update_cell(self, new_cell):
        """
        Update cell content
        """
        old_cell = self.__mat[new_cell.x][new_cell.y]
        self.upd_species(old_cell.species, (-1)*old_cell.group_size)
        self.__mat[new_cell.x][new_cell.y] = new_cell
        self.upd_species(new_cell.species, new_cell.group_size)

    # END update_cell

    def upd_species(self, species, number):
        """
        Update the population of a specie
        """
        if species is None:
            pass
        elif species == 'w':
            self.__w += number
        elif species == 'h':
            self.__h += number
        elif species == 'v':
            self.__v += number

    # END upd_species
        
    def heuristic(self):
        """
        Return the heuristic value of the board
        """
        try:
            return self.__w / self.__v if self.__species == "w" else self.__v / self.__w
        except ZeroDivisionError:
            return 0 # to match the IA requirements
    
    # END heuristic

    def upd_win(self):
        """
        Update the win value
        """
        if self.__species == "w" and self.__w == 0:
            self.__win = -1
        elif self.__species == "v" and self.__v == 0:
            self.__win = -1
        elif self.__species == "w" and self.__v == 0:
            self.__win = 1
        elif self.__species == "v" and self.__w == 0:
            self.__win = 1
    
    # END upd_win
