# -*- coding: utf-8 -*-

# @class Cell

# -- Third-party modules

##
# @brief A tool for cell handling
#


class Cell:

    # ----------------------------------------------------------------------------
    # -- INITIALIZATION
    # ----------------------------------------------------------------------------

    def __init__(self, x, y, species, group_size):
        """
        A tool for cell handling
        """
        self.__x = x
        self.__y = y
        self.__species = species
        self.__group_size = group_size
    # END __init__

    def __copy__(self):
        """
        The copy() method returns a shallow copy of the cell
        """
        other_cell = Cell(self.x, self.y, self.species, self.group_size)
        return other_cell
    # END __copy__

    # ----------------------------------------------------------------------------
    # -- GETTERS AND SETTERS
    # ----------------------------------------------------------------------------

    """
    x_position of the cell in the board.
    """
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x
    # END X
    
    """
    y_position of the cell in the board.
    """
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, y):
        self.__y = y
    # END y

    """
    species of individuals in the cell
    """
    @property
    def species(self):
        return self.__species
    
    @species.setter
    def species(self, species):
        self.__species = species
    # END species
    
    """
    number of individuals in the cell
    """
    @property
    def group_size(self):
        return self.__group_size
    
    @group_size.setter
    def group_size(self, group_size):
        self.__group_size = group_size
    # END group_size