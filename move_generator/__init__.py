class MoveGenerator:
    def __init__(self, board):
        self.__board = board

    def get_possible_moves(self):
        possible_moves = [] # array of Move objects
        friend_cells = self.__board.get_friend_cells()
        for friend_cell in friend_cells:
            possible_moves = possible_moves.concat(self.get_possible_move(friend_cell))
        return possible_moves

    def get_possible_move(self, src_cell):
        possible_moves = []
        board_width = self.__board.get_width()
        board_height = self.__board.get_height()
        x0 = src_cell.get_x()
        y0 = src_cell.get_y()
        ###
        # IMPORTANT
        # For now we do not split our population
        # We only move the entire group contained in our cells
        # TODO? - Enable splitting moves
        ###
        change = Change(src_cell.get_value(), src_cell.get_species())
        if (x0 > 0): # Move left
            dest_cell = self.__board.get_cell((x0 - 1, y0))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
        if (x0 > 0 and y0 > 0): # Move bottom left
            dest_cell = self.__board.get_cell((x0 - 1, y0 - 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
        if (x0 > 0 and y0 < board_height - 1): # Move up left
            dest_cell = self.__board.get_cell((x0 - 1, y0 + 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
        if (y0 < board_height - 1): # Move up
            dest_cell = self.__board.get_cell((x0, y0 + 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
        if (y0 > 0): # Move bottom
            dest_cell = self.__board.get_cell((x0, y0 - 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
        if (x0 < board_width - 1): # Move right
            dest_cell = self.__board.get_cell((x0 + 1, y0))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
        if (x0 < board_width - 1 and y0 < board_height - 1): # Move up right
            dest_cell = self.__board.get_cell((x0 + 1, y0 + 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
        if (x0 < board_width - 1 and ): # Move bottom right
            dest_cell = self.__board.get_cell((x0 + 1, y0 - 1))
            possible_move = Move(src_cell, dest_cell, change)
            possible_moves.append(possible_move)
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
