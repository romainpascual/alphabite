# -*- coding: utf-8 -*-

# @class Board

# -- Third-party modules

# -- Program modules
from .cell import Cell
from copy import copy
from math import inf

##
# @brief A tool for board simulation
#__cell

class Board:
    
    # ----------------------------------------------------------------------------
    # -- CLASS ATTRIBUTES
    # ----------------------------------------------------------------------------

    # Error status
    SUCCESS = 0
    FAILURE = 1

    # ----------------------------------------------------------------------------
    # -- DEFAULT FUNCTIONS
    # ----------------------------------------------------------------------------

    def __init__(
            self,
            x=0,
            y=0):
        # -- Errors
        self.__err_code = Board.FAILURE
        self.__err_msg = "Board.init()"
    
        # Attributs
        self.__X = x
        self.__Y = y
        self.__cells = dict()
        for i in range(self.__X):
            for j in range(self.__Y):
                self.__cells[(i, j)] = Cell(i,j, None, 0)
        self.__species = ""
        self.__h = 0
        self.__v = 0
        self.__w = 0
        self.__win = 0
        self.__friend_cells = dict()

        # -- Errors
        self.__err_code = Board.SUCCESS
        self.__err_msg = ""
    # END __init__

    def __copy__(self):
        """
        The copy() method returns a shallow copy of the board
        """
        # Create a new instance
        other_board = Board()

        # Copy the attributes
        other_board.__n = self.__X
        other_board.__m = self.__Y
        other_board.__cells = self.__cells.copy()
        other_board.__species = self.__species
        other_board.__h = self.__h
        other_board.__v = self.__v
        other_board.__w = self.__w
        other_board.__win = self.__win
        other_board.__friend_cells = self.__friend_cells.copy()

        return other_board
    # END __copy__

    def __repr__(self):
        repr_str = str()
        for j in range(self.__Y):
            for i in range(self.__X):
                cell = self.__cells[(i, j)]
                group_size = cell.group_size
                species = cell.species if cell.species else ' '
                repr_str += '{}{} '.format(group_size, species)
            repr_str += '\n'
        return repr_str
    # END __repr__

    @staticmethod
    def create_from_board(previous_board, cell_list):
        """
        Create a new board from a previous board and a given cell list to change
        """
        new_board = copy(previous_board)
        for cell in cell_list:
            new_board.update_cell(cell)
        new_board.upd_win()
        return new_board
    # END create_from_board

    # ----------------------------------------------------------------------------
    # -- GETTERS AND SETTERS
    # ----------------------------------------------------------------------------

    def build(self, x , y):
        """
        Build the board with the given sizes.
        Can be used to reset the map.
        """
        self.__init__(x,y)
    # END build

    @property
    def width(self):
        """
        Get width
        """
        return self.__X
    # END width

    @property
    def height(self):
        """
        Get height
        """
        return self.__Y
    # END height

    def get_cell(self, pos):
        """
        Return the content of the cell at position(i,j)
        """
        return copy(self.__cells[(pos[0], pos[1])])
    # END get_cell

    @property
    def humans(self):
        """
        Get population of human
        """
        return self.__h
    # END humans

    @property
    def vampires(self):
        """
        Get population of vampire
        """
        return self.__v
    # END vampires

    @property
    def werewolves(self):
        """
        Get population of werewolves
        """
        return self.__w
    # END werewolves

    @property
    def win(self):
        """
        Return the winning status (1 if won, -1 if lost, 0 o.w.)
        """
        return self.__win
    # END win

    @property
    def species(self):
        """
        Return our species
        """
        return self.__species

    @species.setter
    def species(self, species):
        """
        Change the species
        """
        self.__species = species
        for cell in self.__cells.values():
            self.upd_friend_cells(cell)
    # END species

    @property
    def friend_cells(self):
        """
        Return the cells of our specie as a list
        """
        return list(self.__friend_cells.values())
    # END friend_cells

    # ----------------------------------------------------------------------------
    # -- UPDATE
    # ----------------------------------------------------------------------------

    def update(self, upd):
        """
        Update the board according to upd=[(x, y, (species, nb))]
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

        print(repr(self))
    # END update

    def set_species(self, x, y):
        """
        Using the home cell, find out which species we are
        """
        self.__species = self.__cells[(x,y)].species
        for cell in self.__cells.values():
            self.upd_friend_cells(cell)
    # END set_species
    
    def update_cell(self, new_cell):
        """
        Update cell content
        """
        old_cell = self.__cells[(new_cell.x, new_cell.y)]
        self.upd_species(old_cell.species, (-1)*old_cell.group_size)
        self.__cells[(new_cell.x,new_cell.y)] = new_cell
        self.upd_species(new_cell.species, new_cell.group_size)
        self.upd_friend_cells(new_cell)
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

    def upd_friend_cells(self, cell):
        """
        Update the friendly cells
        """
        if cell.species == self.__species:
            self.__friend_cells[(cell.x,cell.y)] = cell
        else:
            self.__friend_cells.pop((cell.x,cell.y), None)
    # END upd_friend_cells

    # ----------------------------------------------------------------------------
    # -- PLAYS
    # ----------------------------------------------------------------------------

    def heuristic(self):
        """
        Return the heuristic value of the board
        """
        try:
            return self.__w / self.__v if self.__species == "w" else self.__v / self.__w
        except ZeroDivisionError:
            return inf # to match the IA requirements 
    # END heuristic

