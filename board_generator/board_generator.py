from board import Board, Cell
from .move_generator import MoveGenerator
from .misc import Misc


class BoardGenerator:
    def __init__(self, src_board, species, prev_move):
        self.__src_board = src_board
        self.__species = species
        self.__move_generator = MoveGenerator(src_board, species, prev_move)

    def get_all_possible_boards(self):
        possible_moves = self.__move_generator.get_all_possible_moves()
        for possible_move in possible_moves:
            for possible_board in self.get_possible_boards(possible_move):
                yield (possible_board, possible_move)  # (Board objects associated with a probability, Move object)

    def get_possible_boards(self, move):
        src_cell = move.src_cell  # Cell object
        dest_cell = move.dest_cell  # Cell object

        change = move.change  # Change object
        moving_group_size = change.value

        if dest_cell.group_size == 0:
            # The dest cell is empty
            # We simply move our guys
            return self.get_simple_move_board(src_cell, dest_cell, moving_group_size)

        if dest_cell.species == src_cell.species:
            # The dest cell contains some of our guys
            # We simply move our guys
            return self.get_simple_move_board(src_cell, dest_cell, moving_group_size)

        if dest_cell.species == 'h':
            if moving_group_size >= dest_cell.group_size:
                # The dest cell contains humans not numerous to survive
                # It looks as if it was initially filled with our guys
                return self.get_simple_move_board(src_cell, dest_cell, moving_group_size)
            else:
                # The dest cell contains humans and they are numerous
                # A random battle happens
                return self.get_all_random_battle_boards(src_cell, dest_cell, moving_group_size)

        if src_cell.species != dest_cell.species:
            if moving_group_size >= 1.5 * dest_cell.group_size:
                # The dest cell contains enemies not numerous to survive
                # It's a slaughter
                return self.get_full_win_board(src_cell, dest_cell, moving_group_size)
            elif dest_cell.group_size >= 1.5 * moving_group_size:
                # The dest cell contains a lot of enemies
                # It's a full defeat
                return self.get_full_defeat_board(src_cell, dest_cell, moving_group_size)
            else:
                # The dest cell contains enemies in a certain number
                # A random battle happens
                return self.get_all_random_battle_boards(src_cell, dest_cell, moving_group_size)

    def get_simple_move_board(self, src_cell, dest_cell, moving_group_size):
        new_src_cell = Cell(src_cell.x, src_cell.y, src_cell.species, src_cell.group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell.x, dest_cell.y, src_cell.species, dest_cell.group_size + moving_group_size)

        new_board = Board.create_from_board(self.__src_board, [new_src_cell, new_dest_cell])

        return [(new_board, 1)]  # (Board, probability)

    def get_full_win_board(self, src_cell, dest_cell, moving_group_size):
        new_src_cell = Cell(src_cell.x, src_cell.y, src_cell.species, src_cell.group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell.x, dest_cell.y, src_cell.species, moving_group_size)

        new_board = Board.create_from_board(self.__src_board, [new_src_cell, new_dest_cell])

        return [(new_board, 1)]  # (Board, probability)

    def get_full_defeat_board(self, src_cell, dest_cell, moving_group_size):
        new_src_cell = Cell(src_cell.x, src_cell.y, src_cell.species, src_cell.group_size - moving_group_size)
        new_dest_cell = Cell(dest_cell.x, dest_cell.y, dest_cell.species, dest_cell.group_size)

        new_board = Board.create_from_board(self.__src_board, [new_src_cell, new_dest_cell])

        return [(new_board, 1)]  # (Board, probability)

    def get_all_random_battle_boards(self, src_cell, dest_cell, moving_group_size):
        if moving_group_size == dest_cell.group_size:
            p = 0.5
            new_boards_src_winning = self.get_random_battle_boards(src_cell, dest_cell, moving_group_size, p, True)
            new_boards_dest_winning = self.get_random_battle_boards(src_cell, dest_cell, moving_group_size, p, False)
        elif moving_group_size < dest_cell.group_size:
            p = moving_group_size / (2 * dest_cell.group_size)
            new_boards_src_winning = self.get_random_battle_boards(src_cell, dest_cell, moving_group_size, p, True)
            new_boards_dest_winning = self.get_random_battle_boards(src_cell, dest_cell, moving_group_size, p, False)
        else:
            p = (moving_group_size / dest_cell.group_size) - 0.5
            new_boards_src_winning = self.get_random_battle_boards(src_cell, dest_cell, moving_group_size, p, True)
            new_boards_dest_winning = self.get_random_battle_boards(src_cell, dest_cell, moving_group_size, p, False)
        return new_boards_src_winning + new_boards_dest_winning

    def get_random_battle_boards(self, src_cell, dest_cell, moving_group_size, p, attacker_is_winner):
        possible_boards = []  # Array of Board objects associated with a probability
        if attacker_is_winner:
            for k in range(src_cell.group_size + 1):
                new_src_cell = Cell(src_cell.x, src_cell.y, src_cell.species, src_cell.group_size - moving_group_size)
                new_dest_cell = Cell(dest_cell.x, dest_cell.y, src_cell.species, k)

                new_board = Board.create_from_board(self.__src_board, [new_src_cell, new_dest_cell])

                # We use the binomial law to compute the probability of surviving
                k_survivor_probability = Misc.p_binom(src_cell.group_size, k, p)

                possible_boards.append((new_board, p * k_survivor_probability))
        else:
            for k in range(dest_cell.group_size + 1):
                new_src_cell = Cell(src_cell.x, src_cell.y, src_cell.species, src_cell.group_size - moving_group_size)
                new_dest_cell = Cell(dest_cell.x, dest_cell.y, dest_cell.species, k)

                new_board = Board.create_from_board(self.__src_board, [new_src_cell, new_dest_cell])

                # We use the binomial law to compute the probability of surviving
                k_survivor_probability = Misc.p_binom(dest_cell.group_size, k, (1 - p))

                possible_boards.append((new_board, (1-p) * k_survivor_probability))

        return possible_boards
