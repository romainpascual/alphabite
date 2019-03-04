# -*- coding: utf-8 -*-

"""
Source : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
Fourni un pseudo code et une explication extensive que j'ai utilisé pour ecrire le code
"""
from board_generator import BoardGenerator
from threading import Thread
import time


class IA(Thread):
    def __init__(self, src_board, max_depth=10):
        Thread.__init__(self)
        self.__src_board = src_board
        self.__best_move = None
        self.__send_mov = None
        self.__max_depth = max_depth
        self.__my_species = None
        self.__enemy_species = None

        self.__shouldRun = True

        self.event = None  # TODO: better event handling to allow for calculation during opponent turn

    def set_species(self, species):
        self.__my_species = species
        self.__enemy_species = 'v' if self.__my_species == 'w' else 'w'

    def alphabeta(self, src_board, prev_move=None, depth=0, isMaximizingPlayer=True, alpha=-float('inf'), beta=float('inf'), max_depth=5):
        """
        Alphabeta AI to choose the best move to play
        :param src_board: Actual Board on which we apply Alphabeta
        :param depth: Actual depth of the graph
        :param isMaximizingPlayer: True if max layer of the minimax and False otherwise
        :param alpha: actual value of alpha in the alphabeta propagation
        :param beta: actual value of beta in the alphabeta propagation
        :param max_depth: Max propagation depth in graph
        :return: best_move
        """

        if depth == max_depth or src_board.is_winning_position:
            return src_board.heuristic(self.__my_species)

        if isMaximizingPlayer:
            generator = BoardGenerator(src_board, self.__my_species, prev_move)
            best_val = -float('inf')
            for board_with_probability, move in generator.get_all_possible_boards():
                board = board_with_probability[0]
                p = board_with_probability[1]
                value = p * self.alphabeta(board, depth + 1, move, False, alpha, beta, max_depth)
                if best_val < value:
                    best_val = value
                    if depth == 0:
                        self.__best_move = move
                if beta <= best_val:
                    return best_val
                alpha = max(alpha, best_val)
            return best_val

        else:
            generator = BoardGenerator(src_board, self.__enemy_species, prev_move)
            best_val = float('inf')
            for board_with_probability, move in generator.get_all_possible_boards():
                board = board_with_probability[0]
                p = board_with_probability[1]
                value = p * self.alphabeta(board, depth + 1, move, True, alpha, beta, max_depth)
                if value < best_val:
                    best_val = value
                    if depth == 0:
                        self.__best_move = move
                if best_val <= alpha:
                    return best_val
                beta = min(beta, best_val)
            return best_val

    def turn_off(self):
        self.__shouldRun = False
        t = 4
        while t:
            print('Turning off IA in {} seconds.'.format(t), end='\r')
            time.sleep(1)
            t -= 1

    def run(self):
        while self.__shouldRun:
            if self.event.wait(4.):
                tic = time.time()
                self.alphabeta(self.__src_board,
                               depth=0,
                               prev_move=None,
                               isMaximizingPlayer=True,
                               alpha=-float('inf'),
                               beta=float('inf'),
                               max_depth=self.__max_depth)
                print("Sending after {:.3f}s".format(time.time()-tic))
                self.__send_mov([self.__best_move.parse_for_socket()])
        print('IA is shutdown.', ' '*20)

    def set_send_mov(self, send_mov_func):
        self.__send_mov = send_mov_func
