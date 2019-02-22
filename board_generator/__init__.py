from .move_generator import MoveGenerator
from .misc import comb

class BoardGenerator:
    def __init__(self, src_board):
        self.__src_board = src_board
        self.__move_generator = MoveGenerator(src_board)

    def get_all_possible_boards(self):
        possible_boards = [] # Array of Board objects associated with a probability
        possible_moves = self.__move_generator.get_all_possible_moves()
        for possible_move in possible_moves:
            possible_boards += self.get_possible_boards(possible_move)
        return possible_boards

    def get_possible_boards(self, move):
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
            # The dest cell is empty
            # We simply move our guys
            return self.get_simple_move_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)

        if (dest_cell_species == src_cell_species):
            # The dest cell contains some of our guys
            # We simply move our guys
            return self.get_simple_move_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)

        if (dest_cell_species == 'h'):
            if (moving_group_size >= dest_cell_group_size):
                # The dest cell contains humans not numerous to survive
                # It looks as if it was initially filled with our guys
                return self.get_simple_move_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
            else:
                # The dest cell contains humans and they are numerous
                # A random battle happens
                return self.get_all_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)

        if (src_cell_species != dest_cell_species):
            if (moving_group_size >= 1.5 * dest_cell_group_size):
                # The dest cell contains enemies not numerous to survive
                # It's a slaughter
                return self.get_full_win_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
            elif (dest_cell_group_size >= 1.5 * moving_group_size):
                # The dest cell contains a lot of enemies
                # It's a full defeat
                return self.get_full_defeat_board(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)
            else:
                # The dest cell contains enemies in a certain number
                # A random battle happens
                return self.get_all_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size)

    def get_simple_move_board(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size):
        new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell_x, dest_cell_y, src_cell_species, dest_cell_group_size + moving_group_size)

        new_board = self.__src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dest_cell)

        return [(new_board, 1)] # (Board, probability)

    def get_full_win_board(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size):
        new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell_x, dest_cell_y, src_cell_species, moving_group_size)

        new_board = self.__src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dest_cell)

        return [(new_board, 1)] # (Board, probability)

    def get_full_defeat_board(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size):
        new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell_x, dest_cell_y, dest_cell_species, dest_cell_group_size)

        new_board = self.__src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dest_cell)

        return [(new_board, 1)] # (Board, probability)

    def get_all_random_battle_boards(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size):
        new_boards_src_winning = None
        new_boards_dest_winning = None
        if (moving_group_size == dest_cell_group_size):
            P = 0.5
            new_boards_src_winning = self.get_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size, P, True)
            new_boards_dest_winning = self.get_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size, P, False)
        elif (moving_group_size < dest_cell_group_size):
            P = moving_group_size / (2 * dest_cell_group_size)
            new_boards_src_winning = self.get_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size, P, True)
            new_boards_dest_winning = self.get_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size, P, False)
        else:
            P = (moving_group_size / dest_cell_group_size) - 0.5
            new_boards_src_winning = self.get_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size, P, True)
            new_boards_dest_winning = self.get_random_battle_boards(src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size, P, False)
        possible_boards = new_boards_src_winning + new_boards_dest_winning
        return possible_boards

    def get_random_battle_boards(self, src_cell_x, src_cell_y, dest_cell_x, dest_cell_y, src_cell_group_size, dest_cell_group_size, moving_group_size, P, attacker_is_winner):
        possible_boards = [] # Array of Board objects associated with a probability
        if (attacker_is_winner):
            for k in range(src_cell_group_size + 1):
                new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
                new_dest_cell = Cell(dest_cell_x, dest_cell_y, src_cell_species, k)

                new_board = self.__src_board.set_cell(new_src_cell)
                new_board = new_board.set_cell(new_dest_cell)

                # We use the binomial law to compute the probability of surviving
                k_survivor_probability = comb(src_cell_group_size, k) * (P**k) * ((1-P)**(src_cell_group_size-k))
                possible_boards.append((new_board, P * k_survivor_probability))
        else:
            for k in range(dest_cell_group_size + 1):
                new_src_cell = Cell(src_cell_x, src_cell_y, src_cell_species, src_cell_group_size - moving_group_size)
                new_dest_cell = Cell(dest_cell_x, dest_cell_y, dest_cell_species, k)

                new_board = self.__src_board.set_cell(new_src_cell)
                new_board = new_board.set_cell(new_dest_cell)

                k_survivor_probability = comb(dest_cell_group_size, k) * ((1-P)**k) * ((P)**(dest_cell_group_size-k))
                possible_boards.append((new_board, P * k_survivor_probability))

        return possible_boards
