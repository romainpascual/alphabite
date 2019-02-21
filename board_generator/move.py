class Move:
    def __init__(self, src_cell, dest_cell, change):
        self.__src_cell = src_cell # Cell object
        self.__dest_cell = dest_cell # Cell object
        self.__change = change # Change object

    def exec(self, board):
        new_board = board.exec_move_src(self.__src_cell, self.__change)
        new_board = new_board.exec_move_dest(self.__dest_cell, self.__change)
        return new_board
