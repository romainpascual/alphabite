from move_generator import MoveGenerator

class BoardGenerator:
    def __init__(self, src_board):
        self.__src_board = src_board
        self.__move_generator = MoveGenerator(src_board)

    def get_possible_boards(self):
        possible_moves = self.__move_generator.get_possible_moves()
