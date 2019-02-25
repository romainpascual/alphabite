# -*- coding: utf-8 -*-

# @class Cell

# -- Third-party modules

##
# @brief A tool for cell handling
#

class Cell( object ):

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

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_species(self):
        return self.__species

    def get_group_size(self):
        return self.__group_size 
    
    def set_x(self, x):
        self.__x = x
    
    def set_y(self, y):
        self.__y = y