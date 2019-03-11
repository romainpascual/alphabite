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
        self.__size = (x+y)/2
        self._cells = dict()
        for i in range(self.__X):
            for j in range(self.__Y):
                self._cells[(i, j)] = Cell(i, j, None, 0)
        self.__h = 0
        self.__v = 0
        self.__w = 0
        self.__h_cells = dict()
        self.__v_cells = dict()
        self.__w_cells = dict()

        self.__vh_min = (inf, None, None)
        self.__wh_min = (inf, None, None)
        self.__vw_min = (inf, None, None)

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
        other_board.__size == self.__size
        other_board._cells = self._cells.copy()
        other_board.__h = self.__h
        other_board.__v = self.__v
        other_board.__w = self.__w
        other_board.__h_cells = self.__h_cells.copy()
        other_board.__v_cells = self.__v_cells.copy()
        other_board.__w_cells = self.__w_cells.copy()
        other_board.__vh_min = self.__vh_min
        other_board.__wh_min = self.__wh_min
        other_board.__vw_min = self.__vw_min

        return other_board
    # END __copy__

    def __repr__(self):
        repr_str = str()
        for j in range(self.__Y):
            for i in range(self.__X):
                cell = self._cells[(i, j)]
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
        return new_board
    # END create_from_board

    # ----------------------------------------------------------------------------
    # -- GETTERS AND SETTERS
    # ----------------------------------------------------------------------------

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

    @property
    def size(self):
        """
        Get size of the board, used to get heuristic value independant from board size
        """
        return self.__size

    def get_cell(self, pos):
        """
        Return the content of the cell at position(i,j)
        """
        return copy(self._cells[(pos[0], pos[1])])
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
    def h_cells(self):
        """
        Return the cells of humans as a list
        """
        return [copy(cell) for cell in self.__h_cells.values()]
    # END h_cells

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
    # END update

    def update_cell(self, new_cell):
        """
        Update cell content
        """
        x = new_cell.x
        y =  new_cell.y
        old_cell = self._cells[(x, y)]

        # process the previous cell
        self.delete_cell_update_dist(old_cell)
        if old_cell.species == 'h':
            self.__h -= old_cell.group_size
            self.__h_cells.pop((x,y), None)
        elif old_cell.species == 'v':
            self.__v -= old_cell.group_size
            self.__v_cells.pop((x,y), None)
        elif old_cell.species == 'w':
            self.__w -= old_cell.group_size
            self.__w_cells.pop((x,y), None)
        
        # process the new cell
        self.create_cell_update_dist(new_cell)
        if new_cell.species == 'h':
            self.__h += new_cell.group_size
            self.__h_cells[(x,y)] = new_cell
        elif new_cell.species == 'v':
            self.__v += new_cell.group_size
            self.__v_cells[(x,y)] = new_cell
        elif new_cell.species == 'w':
            self.__w += new_cell.group_size
            self.__w_cells[(x,y)] = new_cell

        self._cells[(x, y)] = new_cell
    # END update_cell

    # ----------------------------------------------------------------------------
    # -- DISTANCE
    # ----------------------------------------------------------------------------
    def min_distance_from_to(self, cell, species):
        """
        Compute the minimal distance between cell to cells of the given species
        Return dist, target_cell
        
        The way it is implemented, we can not have cell beeing human
        """
        target_cells = []
        if species == 'h':
            target_cells = self.h_cells

            # handle empty cell list
            if len(target_cells) == 0:
                return inf, None

            min_dist = inf
            t = None
            for t_cell in target_cells:
                    d = cell.dist_to(t_cell)
                    if d < min_dist and t_cell.group_size <= cell.group_size:
                        min_dist = d
                        t = t_cell
            return (min_dist, t)


        else:
            if species == 'v':
                target_cells = self.v_cells
            elif species == 'w':
                target_cells = self.w_cells

            # handle empty cell list
            if len(target_cells) == 0:
                return inf, None

            min_dist = inf
            t = None
            for t_cell in target_cells:
                    d = cell.dist_to(t_cell)
                    if d < min_dist:
                        min_dist = d
                        t = t_cell
            return (min_dist, t)
    # END min_distance_between_species

    def min_distance_species(self, source_species, target_species):
        """
        Compute the minimal distance between cells of two species
        Return dist, source_cell, target_cell

        The way it is implemented, we can not have source_specie beeing human
        """
        if source_species == 'h':
            source_cells = self.h_cells
        elif source_species == 'v':
            source_cells = self.v_cells
        elif source_species == 'w':
            source_cells = self.w_cells

        # handle empty cell list
        if len(source_cells) == 0:
            return inf, None

        min_dist = inf
        s = None
        t = None
        for s_cell in source_cells:
                d, t_cell = self.min_distance_from_to(s_cell, target_species)
                if d < min_dist:
                    min_dist, s, t = d, s_cell, t_cell
        return (min_dist, s, t)
    # END min_distance_species


    def delete_cell_update_dist(self, cell):
        """
        When cell is deleted, update the min_distances
        """
        # humans
        if cell.species == 'h':

            # vampires
            if self.__vh_min[2] == cell:
                self.__vh_min = self.min_distance_species('v','h')

            # werewolvev
            if self.__wh_min[2] == cell:
                self.__wh_min = self.min_distance_species('w','h')

        # vampires
        elif cell.species == 'v':

            # humans
            if self.__vh_min[1] == cell:
                self.__vh_min = self.min_distance_species('v','h')

            # werewolves
            if self.__vw_min[1] == cell:
                self.__vw_min = self.min_distance_species('v','w')

        # werewolves
        elif cell.species == 'w':

            # humans
            if self.__wh_min[1] == cell:
                self.__wh_min = self.min_distance_species('w','h')

            # vampires
            if self.__vw_min[2] == cell:
                self.__vw_min = self.min_distance_species('v','w')
    # END delete_cell_update_dist

    def create_cell_update_dist(self, cell):
        """
        When cell is created, update the min_distances
        """
        # humans
        if cell.species == 'h':

            # vampires
            to_vampire = self.min_distance_from_to(cell,'v')
            if self.__vh_min[0] > to_vampire[0]:
                self.__vh_min = (to_vampire[0], to_vampire[1], cell)

            # werewolves
            to_werewolf = self.min_distance_from_to(cell,'w')
            if self.__wh_min[0] > to_werewolf[0]:
                self.__wh_min = (to_werewolf[0], to_werewolf[1], cell)

        # vampires
        elif cell.species == 'v':

            # humans
            to_human = self.min_distance_from_to(cell,'h')
            if self.__vh_min[0] > to_human[0]:
                self.__vh_min = (to_human[0], cell, to_human[1])

            # werewolves
            to_werewolf = self.min_distance_from_to(cell,'w')
            if self.__vw_min[0] > to_werewolf[0]:
                self.__vw_min = (to_werewolf[0], cell, to_werewolf[1])

        # werewolves
        elif cell.species == 'w':

            # humans
            to_human = self.min_distance_from_to(cell,'h')
            if self.__wh_min[0] > to_human[0]:
                self.__wh_min = (to_human[0], cell, to_human[1])

            # vampire
            to_vampire = self.min_distance_from_to(cell,'v')
            if self.__vw_min[0] > to_vampire[0]:
                self.__vw_min = (to_vampire[0], to_vampire[1], cell)
    # END create_cell_update_dist

    # ----------------------------------------------------------------------------
    # -- PLAYS
    # ----------------------------------------------------------------------------

    @property
    def is_winning_position(self):
        """
        Determine whether the game is finished
        """
        if self.__v == 0 or self.__w == 0:
            return True
        else:
            return False
    # END is_winning_position

    @staticmethod
    def f(ratio):
        """
        function to evaluate the weight to give to the distance between the two closest cell on different species.
        """
        if ratio < 2. / 3.:
            return 1.
        elif ratio > 3. / 2.:
            return -1.
        else:
            return (6. * ratio * ratio - 25. * ratio + 19) / 5.

    def heuristic(self, species, win_value=50, lose_value=-100, alpha_specie=20, alpha_dist=1, alpha_human=10):
        """
        Return the heuristic value of the board, assuming max player is playing species
        """

        if species == "w":
            if self.__w == 0:
                return lose_value, -1
            elif self.__v == 0:
                return win_value, 1
            else:
                # we want to maximize the ratio of our specie over the other specie
                specie_value = (self.__w - self.__v)/self.__w

                # if the ratio is > 1, we want to minimze the distance
                dist_value = self.__vw_min[0] * self.f(float(self.__vw_min[2].group_size)/float(self.__vw_min[1].group_size))

                # we want to maximize the distance for between the other specie and a human cell
                human_value = self.__vh_min[0]
                # we want to minimize the distance between our species and a human cell
                human_value -= self.__wh_min[0]
        
        else:
            if self.__v == 0:
                return lose_value, -1
            elif self.__w == 0:
                return win_value, 1
            else:
                specie_value = (self.__v - self.__w)/self.__v
                dist_value = (self.__vw_min[0] * self.f(float(self.__vw_min[1].group_size)/float(self.__vw_min[2].group_size))) / self.__size
                human_value = (self.__wh_min[0] - self.__vh_min[0])/ self.__size
        #print("specie_value: {} -- dist_value: {} -- human_value: {}".format(specie_value, dist_value, human_value))
        output_value = specie_value*alpha_specie + dist_value*alpha_dist + human_value*alpha_human
        #print("output_value: {}".format(output_value))
        return output_value, 0
    # END heuristic

