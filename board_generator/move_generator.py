from .move import Move
from .change import Change


class MoveGenerator:
    def __init__(self, board, species, prev_move):
        self.__board = board
        self.__species = species
        self.__prev_move = prev_move

    def get_all_possible_moves(self):
        # Return an array of move objects that the IA can possibly perform given the state of the board
        possible_moves = [] # array of Move objects
        friend_cells = self.__board.get_cells(self.__species)
        for friend_cell in friend_cells:
            possible_moves = possible_moves + self.get_possible_moves(friend_cell)
        return possible_moves

    def get_possible_moves(self, src_cell):
        ###
        # IMPORTANT
        # For now we do not split our population
        # We only move the entire group contained in our cells
        # TODO? - Enable splitting moves
        ###
        change = Change(src_cell.group_size, src_cell.species)

        return self.get_possible_moves_with_change(src_cell, change)

    def get_possible_moves_with_change(self, src_cell, change):
        # Todo: doc this
        possible_moves = []
        board_width = self.__board.width
        board_height = self.__board.height
        x0 = src_cell.x
        y0 = src_cell.y
        prev_cell = self.__prev_move.src_cell
        delta_x = x0 - prev_cell.x
        delta_y = y0 - prev_cell.y

        if x0 > 0 and y0 > 0
            and not (delta_x == 1 and delta_y == 1)
            and not (delta_x == 0 and delta_y == 1)
            and not (delta_x == 1 and delta_y == 0):  # Move up left
            dest_cell = self.__board.get_cell((x0 - 1, y0 - 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        if x0 < board_width - 1 and y0 > 0
            and not (delta_x == 0 and delta_y == 1)
            and not (delta_x == -1 and delta_y == 0)
            and not (delta_x == -1 and delta_y == 1):  # Move up right
            dest_cell = self.__board.get_cell((x0 + 1, y0 - 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        if x0 > 0 and y0 < board_height - 1
            and not (delta_x == 1 and delta_y == 0)
            and not (delta_x == 1 and delta_y == -1)
            and not (delta_x == 0 and delta_y == -1):  # Move down left
            dest_cell = self.__board.get_cell((x0 - 1, y0 + 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        if x0 < board_width - 1 and y0 < board_height - 1
            and not (delta_x == -1 and delta_y == 0)
            and not (delta_x == -1 and delta_y == -1)
            and not (delta_x == 0 and delta_y == -1):  # Move down right
            dest_cell = self.__board.get_cell((x0 + 1, y0 + 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        if x0 > 0
            and not (delta_x == 1 and delta_y == 1)
            and not (delta_x == 1 and delta_y == 0)
            and not (delta_x == 1 and delta_y == -1): # Move left
            dest_cell = self.__board.get_cell((x0 - 1, y0))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        if x0 < board_width - 1 and delta_x > 0
            and not (delta_x == -1 and delta_y == 1)
            and not (delta_x == -1 and delta_y == 0)
            and not (delta_x == -1 and delta_y == -1): # Move right
            dest_cell = self.__board.get_cell((x0 + 1, y0))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        if y0 > 0
            and not (delta_x == 0 and delta_y == 1)
            and not (delta_x == 1 and delta_y == 1)
            and not (delta_x == -1 and delta_y == 1):  # Move up
            dest_cell = self.__board.get_cell((x0, y0 - 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        if y0 < board_height - 1
            and not (delta_x == 0 and delta_y == -1)
            and not (delta_x == 1 and delta_y == -1)
            and not (delta_x == -1 and delta_y == -1):  # Move down
            dest_cell = self.__board.get_cell((x0, y0 + 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)

        return possible_moves
