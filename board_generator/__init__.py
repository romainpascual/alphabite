from .move_generator import MoveGenerator
from .misc import comb


class BoardGenerator:
    def __init__(self, src_board):
        self.__src_board = src_board
        self.__move_generator = MoveGenerator(src_board)

    def get_all_possible_boards(self):
        possible_boards = []  # Array of tuples (Board objects associated with a probability, Move object)
        possible_moves = self.__move_generator.get_all_possible_moves()
        for possible_move in possible_moves:
            possible_boards += (self.get_possible_boards(possible_move), possible_move)
        return possible_boards

    def get_possible_boards(self, move):
        src_cell = move.get_src_cell()  # Cell object
        dst_cell = move.get_dst_cell()  # Cell object

        change = move.get_change()  # Change object
        moving_group_size = change.get_value()

        if dst_cell.get_group_size() == 0:
            # The dst cell is empty
            # We simply move our guys
            return self.get_simple_move_board(src_cell, dst_cell, moving_group_size)

        if dst_cell.get_species() == src_cell.get_species():
            # The dst cell contains some of our guys
            # We simply move our guys
            return self.get_simple_move_board(src_cell, dst_cell, moving_group_size)

        if dst_cell.get_species() == 'h':
            if moving_group_size >= dst_cell.get_group_size():
                # The dst cell contains humans not numerous to survive
                # It looks as if it was initially filled with our guys
                return self.get_simple_move_board(src_cell, dst_cell, moving_group_size)
            else:
                # The dst cell contains humans and they are numerous
                # A random battle happens
                return self.get_all_random_battle_boards(src_cell, dst_cell, moving_group_size)

        if src_cell.get_species() != dst_cell.get_species():
            if moving_group_size >= 1.5 * dst_cell.get_group_size():
                # The dst cell contains enemies not numerous to survive
                # It's a slaughter
                return self.get_full_win_board(src_cell, dst_cell, moving_group_size)
            elif dst_cell.get_group_size() >= 1.5 * moving_group_size:
                # The dst cell contains a lot of enemies
                # It's a full defeat
                return self.get_full_defeat_board(src_cell, dst_cell, moving_group_size)
            else:
                # The dst cell contains enemies in a certain number
                # A random battle happens
                return self.get_all_random_battle_boards(src_cell, dst_cell, moving_group_size)

    def get_simple_move_board(self, src_cell, dst_cell, moving_group_size):
        new_src_cell = Cell(
            src_cell.get_x(),
            src_cell.get_y(),
            src_cell.get_species(),
            src_cell.get_group_size() - moving_group_size)
        new_dst_cell = Cell(
            dst_cell.get_x(),
            dst_cell.get_y(),
            src_cell.get_species(),
            dst_cell.get_group_size() + moving_group_size)

        new_board = self.__src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dst_cell)

        return [(new_board, 1)]  # (Board, probability)

    def get_full_win_board(self, src_cell, dst_cell, moving_group_size):
        new_src_cell = Cell(
            src_cell.get_x(),
            src_cell.get_y(),
            src_cell.get_species(),
            src_cell.get_group_size() - moving_group_size)
        new_dst_cell = Cell(
            dst_cell.get_x(),
            dst_cell.get_y(),
            src_cell.get_species(),
            moving_group_size)

        new_board = self.__src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dst_cell)

        return [(new_board, 1)]  # (Board, probability)

    def get_full_defeat_board(self, src_cell, dst_cell, moving_group_size):
        new_src_cell = Cell(
            src_cell.get_x(),
            src_cell.get_y(),
            src_cell.get_species(),
            src_cell.get_group_size() - moving_group_size)
        new_dst_cell = Cell(
            dst_cell.get_x(),
            dst_cell.get_y(),
            dst_cell.get_species(),
            dst_cell.get_group_size())

        new_board = self.__src_board.set_cell(new_src_cell)
        new_board = new_board.set_cell(new_dst_cell)

        return [(new_board, 1)]  # (Board, probability)

    def get_all_random_battle_boards(self, src_cell, dst_cell, moving_group_size):
        if moving_group_size == dst_cell.get_group_size():
            p = 0.5
            new_boards_src_winning = self.get_random_battle_boards(src_cell, dst_cell, moving_group_size, p, True)
            new_boards_dst_winning = self.get_random_battle_boards(src_cell, dst_cell, moving_group_size, p, False)
        elif moving_group_size < dst_cell.get_group_size():
            p = moving_group_size / (2 * dst_cell.get_group_size())
            new_boards_src_winning = self.get_random_battle_boards(src_cell, dst_cell, moving_group_size, p, True)
            new_boards_dst_winning = self.get_random_battle_boards(src_cell, dst_cell, moving_group_size, p, False)
        else:
            p = (moving_group_size / dst_cell.get_group_size()) - 0.5
            new_boards_src_winning = self.get_random_battle_boards(src_cell, dst_cell, moving_group_size, p, True)
            new_boards_dst_winning = self.get_random_battle_boards(src_cell, dst_cell, moving_group_size, p, False)
        return new_boards_src_winning + new_boards_dst_winning

    def get_random_battle_boards(self, src_cell, dst_cell, moving_group_size, p, attacker_is_winner):
        possible_boards = []  # Array of Board objects associated with a probability
        if attacker_is_winner:
            for k in range(src_cell.get_group_size() + 1):
                new_src_cell = Cell(
                    src_cell.get_x(),
                    src_cell.get_y(),
                    src_cell.get_species(),
                    src_cell.get_group_size() - moving_group_size)
                new_dst_cell = Cell(
                    dst_cell.get_x(),
                    dst_cell.get_y(),
                    src_cell.get_species(),
                    k)

                new_board = self.__src_board.set_cell(new_src_cell)
                new_board = new_board.set_cell(new_dst_cell)

                # We use the binomial law to compute the probability of surviving
                k_survivor_probability = \
                    comb(src_cell.get_group_size(), k) * (p**k) * ((1-p)**(src_cell.get_group_size()-k))
                possible_boards.append((new_board, p * k_survivor_probability))
        else:
            for k in range(dst_cell.get_group_size() + 1):
                new_src_cell = Cell(
                    src_cell.get_x(),
                    src_cell.get_y(),
                    src_cell.get_species(),
                    src_cell.get_group_size() - moving_group_size)
                new_dst_cell = Cell(
                    dst_cell.get_x(),
                    dst_cell.get_y(),
                    dst_cell.get_species(),
                    k)

                new_board = self.__src_board.set_cell(new_src_cell)
                new_board = new_board.set_cell(new_dst_cell)

                k_survivor_probability = \
                    comb(dst_cell.get_group_size(), k) * ((1-p)**k) * (p**(dst_cell.get_group_size()-k))
                possible_boards.append((new_board, p * k_survivor_probability))

        return possible_boards
