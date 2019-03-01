# -*- coding: utf-8 -*-

# @class Board

# -- Third-party modules

# -- Program modules
from .cell import Cell
from copy import copy
from math import inf

##
# @brief A tool for board simulation
#

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
        self.__h = 0
        self.__v = 0
        self.__w = 0
        self.__v_cells = dict()
        self.__w_cells = dict()

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
        other_board.__X = self.__X
        other_board.__Y = self.__Y
        other_board.__cells = self.__cells.copy()
        other_board.__h = self.__h
        other_board.__v = self.__v
        other_board.__w = self.__w
        other_board.__v_cells = self.__v_cells.copy()
        other_board.__w_cells = self.__w_cells.copy()

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
    def v_cells(self):
        """
        Return the cells of vampires as a list
        """
        return [copy(cell) for cell in self.__v_cells.values()]
    # END v_cells

    @property
    def w_cells(self):
        """
        Return the cells of werevolves as a list
        """
        return [copy(cell) for cell in self.__w_cells.values()]
    # END w_cells
    
    def get_cells(self, species):
        """
        Return the cells of species as a list
        """
        if species == 'v':
            return self.v_cells
        elif species == 'w':
            return self.w_cells
    # END get_cells

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

        # -- Errors
        self.__err_code = Board.SUCCESS
        self.__err_msg = ""

        print(repr(self))
    # END update

    
    def update_cell(self, new_cell):
        """
        Update cell content
        """
        x = new_cell.x
        y =  new_cell.y
        old_cell = self.__cells[(x, y)]

        # process the previous cell
        if old_cell.species is None:
            pass
        elif old_cell.species == 'h':
            self.__h -= old_cell.group_size
        elif old_cell.species == 'v':
            self.__v -= old_cell.group_size
            self.__v_cells.pop((x,y), None)
        elif old_cell.species == 'w':
            self.__w -= old_cell.group_size
            self.__w_cells.pop((x,y), None)
        
        # process the new cell
        if new_cell.species is None:
            pass
        elif new_cell.species == 'h':
            self.__h += new_cell.group_size
        elif new_cell.species == 'v':
            self.__v += new_cell.group_size
            self.__v_cells[(x,y)] = new_cell
        elif new_cell.species == 'w':
            self.__w += new_cell.group_size
            self.__w_cells[(x,y)] = new_cell

        self.__cells[(x,y)] = new_cell
    # END update_cell

    # ----------------------------------------------------------------------------
    # -- PLAYS
    # ----------------------------------------------------------------------------

    def heuristic(self, species):
        """
        Return the heuristic value of the board, assuming max player is playing species
        """
        try:
            return self.__w / self.__v if species == "w" else self.__v / self.__w
        except ZeroDivisionError:
            return inf # to match the IA requirements 
    # END heuristic

