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
            new_board.updateCell(cell)
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
    def m(self):
        """
        Get width
        """
        return self.__m
    
    # END m

    @property
    def n(self):
        """
        Get height
        """
        return self.__n
    
    # END n

    def getCell(self, i, j):
        """
        Return the content of the cell at position(i,j)
        """
        return self.__mat[i][j]

    # END getCell

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
            self.updateCell(newCell)

        # -- Errors
        self.__err_code = Board.SUCCESS
        self.__err_msg = ""

    # END update

    def updateCell(self, newCell):
        self.__mat[newCell.x][newCell.y] = newCell
    
    # END updateCell

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

    def updSpecies(self, species, number):
        if(species == None):
            pass
        elif(species == 'w'):
            self.__w += number
        elif(species == 'h'):
            self.__h += number
        elif (species == 'v'):
            self.__v += number
    
    # END updSpecies
        
    def heuristic(self):
        """
        return the heuristic value of the board
        """
        try:
            return self.__w / self.__v if self.__species == "w" else self.__v / self.__w
        except ZeroDivisionError:
            return 0 # to match the IA requirements
    
    # END heuristic