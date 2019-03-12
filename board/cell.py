# -*- coding: utf-8 -*-

# @class Cell

# -- Third-party modules
import math

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
        self.__group_size = group_size
        if group_size == 0:
            self.__species = None
        else:
            self.__species = species
    # END __init__

    def __copy__(self):
        """
        The copy() method returns a shallow copy of the cell
        """
        other_cell = Cell(self.x, self.y, self.species, self.group_size)
        return other_cell
    # END __copy__

    def __eq__(self, other):
        """
        return self==other.
        """
        return (
            self.__class__ == other.__class__
            and self.__x == other.__x
            and self.__y == other.__y
            and self.__species == other.__species
            and self.__group_size == other.__group_size
        )

    def __lt__(self, other):
        """
        return self < other.
        """
        return (self.__x < other.__x
            or (self.__x == other.__x and self.__y < other.__y)
        )

    def __le__(self, other):
        """
        return self <= other
        """
        return self == other or self < other
    
    def __gt__(self, other):
        """
        return self > other
        """
        return not self <= other

    def __ge__(self, other):
        """
        return self >= other
        """
        return not self < other

    def __repr__(self):
        return "[Cell = ({},{}), specie is {}, group size = {}]".format(self.x, self.y, self.species, self.group_size)

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

    # ----------------------------------------------------------------------------
    # -- AUX
    # ----------------------------------------------------------------------------
    
    def dist_to(self, other):
        """
        Compute the distance between two cells.
        The distance is computed as the number of moves for a group to go from a cell
        to the other.
        """
        if not isinstance(other,Cell):
            return
        x_dist = abs(self.x - other.x)
        y_dist = abs(self.y - other.y)
        return max(x_dist, y_dist)
    # END dist_to