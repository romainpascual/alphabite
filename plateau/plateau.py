# -*- coding: utf-8 -*-

# @class Board

# -- Third-party modules
import numpy

##
# @brief A tool for board simulation?
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
            n,
            m,
            cell2cell,
            p_cell2cell):
    
        # Attributs
        self.n = n
        self.m = m
        self.cell2cell = cell2cell
        self.p_cell2cell = p_cell2cell

        # -- Errors
        self.err_code = Board.SUCCESS
        self.err_msg = ""

    # END def __init__

    def buildFromSocket(self, data):
        pass

    # ----------------------------------------------------------------------------
    # -- GETTERS AND SETTERS
    # ----------------------------------------------------------------------------

