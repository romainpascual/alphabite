from move_generator import MoveGenerator

class BoardGenerator:
    def __init__(self, src_board):
        self.__src_board = src_board
        self.__move_generator = MoveGenerator(src_board)

    def get_all_possible_boards(self):
        possible_boards = [] # Array of Board objects associated with a probability
        possible_moves = self.__move_generator.get_all_possible_moves()
        for possible_move in possible_moves:
            possible_boards = possible_boards + self.get_possible_boards(possible_move)
        return possible_boards

    def get_possible_boards(self, move):
        possible_boards = [] # Array of Board objects associated with a probability

        src_cell = move.get_src_cell() # Cell object
        src_cell_x = src_cell.get_x()
        src_cell_y = src_cell.get_y()
        src_cell_group_size = src_cell.get_group_size()
        src_cell_species = src_cell.get_species()

        dest_cell = move.get_dest_cell() # Cell object
        dest_cell_x = dest_cell.get_x()
        dest_cell_y = dest_cell.get_y()
        dest_cell_group_size = dest_cell.get_group_size()
        dest_cell_species = dest_cell.get_species()

        change = move.get_change() # Change object
        moving_group_size = change.get_value()

        if (dest_cell_group_size == 0):
            new_board = self.get_simple_move_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
            return [new_board]

        if (dest_cell_species == src_cell_species):
            new_board = self.get_simple_move_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
            return [new_board]

        if (dest_cell_species == 'h'):
            if (moving_group_size >= dest_cell_group_size):
                new_board = self.get_simple_move_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
                return [new_board]

            else:
                if (moving_group_size == dest_cell_group_size):
                    P = 0.5
                    # possible_boards.append([new_board_src_winning, P])
                    # possible_boards.append([new_board_dest_winning, 1-P])
                    return possible_boards
                elif (moving_group_size < dest_cell_group_size):
                    P = moving_group_size / (2 * dest_cell_group_size)
                    # possible_boards.append([new_board_src_winning, P])
                    # possible_boards.append([new_board_dest_winning, 1-P])
                    return possible_boards
                else:
                    P = (moving_group_size / dest_cell_group_size) - 0.5
                    # possible_boards.append([new_board_src_winning, P])
                    # possible_boards.append([new_board_dest_winning, 1-P])
                    return possible_boards

        if (src_cell_species != dest_cell_species):
            if (moving_group_size >= 1.5 * dest_cell_group_size):
                new_board = self.get_full_win_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
                return [new_board]

            elif (dest_cell_group_size >= 1.5 * moving_group_size):
                new_board = self.get_full_defeat_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
                return [new_board]

            else:
                if (moving_group_size == dest_cell_group_size):
                    P = 0.5
                    # possible_boards.append([new_board_src_winning, P])
                    # possible_boards.append([new_board_dest_winning, 1-P])
                    return possible_boards
                elif (moving_group_size < dest_cell_group_size):
                    P = moving_group_size / (2 * dest_cell_group_size)
                    # possible_boards.append([new_board_src_winning, P])
                    # possible_boards.append([new_board_dest_winning, 1-P])
                    return possible_boards
                else:
                    P = (moving_group_size / dest_cell_group_size) - 0.5
                    # possible_boards.append([new_board_src_winning, P])
                    # possible_boards.append([new_board_dest_winning, 1-P])
                    return possible_boards

    def get_simple_move_board(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size):
        new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell_x, dest_cell_y, src_cell_species, dest_cell_group_size + moving_group_size)

        new_board = src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dest_cell)

        return (new_board, 1) # (Board, probability)

    def get_full_win_board(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size):
        new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell_x, dest_cell_y, src_cell_species, moving_group_size)

        new_board = src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dest_cell)

        return (new_board, 1) # (Board, probability)

    def get_full_defeat_board(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size):
        new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell_x, dest_cell_y, dest_cell_species, dest_cell_group_size)

        new_board = src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dest_cell)

        return (new_board, 1) # (Board, probability)
