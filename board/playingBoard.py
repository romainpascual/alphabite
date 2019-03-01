# -*- coding: utf-8 -*-

# @class PlayingBoard

# -- Third-party modules

# -- Program modules
from .cell import Cell
from copy import copy
from math import inf
from .board import Board

##
# @brief A tool to handle the playing board
#

class PlayingBoard( Board ):

    # ----------------------------------------------------------------------------
    # -- DEFAULT FUNCTIONS
    # ----------------------------------------------------------------------------

    def __init__(self):
        """
        A tool to handle the playing board
        """
        super().__init__(self)

        # Attributs
        self.__species = ""    
    # END init

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
    # END species

    def set_species(self, x, y):
        """
        Using the home cell, find out which species we are
        """
        self.__species = self.__cells[(x,y)].species
    # END set_specie

    @property
    def friend_cells(self):
        """
        Return the friendly cells as a list
        """
        if self.__species == 'v':
            return super().v_cells
        elif self.__species == 'w':
            return super().w_cells
    # END friend_cells
