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
        self.__x = x
        self.__y = y
        self.__species = species
        self.__group_size = group_size

    # END def __init__

    # ----------------------------------------------------------------------------
    # -- GETTERS AND SETTERS
    # ----------------------------------------------------------------------------

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x
    
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def species(self):
        return self.__species
    
    @species.setter
    def species(self, species):
        self.__species = species
    
    @property
    def group_size(self):
        return self.__group_size
    
    @group_size.setter
    def group_size(self, group_size):
        self.__group_size = group_size