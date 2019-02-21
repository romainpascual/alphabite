class MoveGenerator:
    def __init__(self, board):
        self.__board = board

    def get_possible_moves(self):
        possible_moves = [] # array of Move objects
        friend_cells = self.__board.get_friend_cells()
        for friend_cell in friend_cells:
            # TODO possible_move = ...
            # possible_moves.append(possible_move)
        return possible_moves


class Move:
    def __init__(self, src_cell, dest_cell, change):
        self.__src_cell = src_cell # Cell object
        self.__dest_cell = dest_cell # Cell object
        self.__change = change # Change object

    def exec(self, board):
        new_board = board.exec_move_src(self.__src_cell, self.__change)
        new_board = new_board.exec_move_dest(self.__dest_cell, self.__change)
        return new_board

class Change:
    def __init__(self, value, species):
        self.__value = value # 0, 1, 2, etc...
        self.__species = species # 'v', 'w', 'h', None
