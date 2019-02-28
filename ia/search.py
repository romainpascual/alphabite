# -*- coding: utf-8 -*-

"""
Source : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
Fourni un pseudo code et une explication extensive que j'ai utilisé pour ecrire le code
"""
from board_generator import BoardGenerator
from threading import Thread
import time


class IA(Thread):
    def __init__(self, src_board, max_depth=5):
        Thread.__init__(self)
        self.__src_board = src_board
        self.__best_move = None
        self.__generator = BoardGenerator(src_board)
        self.__send_mov = None
        self.__max_depth = max_depth

        self.event = None  # TODO: better event handling to allow for calculation during opponent turn

    def alphabeta(self, src_board, depth=0, isMaximizingPlayer=True, alpha=-float('inf'), beta=float('inf'), max_depth=5):
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
        if src_board.win == 1: # on arrête si on a gagné
            return float('inf')

        if src_board.win == -1: # on arrête si on a perdu aussi
            return -float('inf')

        if depth == max_depth:
            return src_board.heuristic()

        if isMaximizingPlayer:
            best_val = -float('inf')
            for board, move in self.__generator.get_all_possible_boards():
                board = board[0][0]
                value = self.alphabeta(board, depth + 1, False, alpha, beta, max_depth)
                if best_val < value:
                    best_val = value
                    if depth == 0:
                        self.__best_move = move
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            return best_val

        else:
            best_val = float('inf')
            for board, move in self.__generator.get_all_possible_boards():
                board = board[0][0]
                value = self.alphabeta(board, depth + 1, True, alpha, beta, max_depth)
                if best_val < value:
                    best_val = value
                    if depth == 0:
                        self.__best_move = move
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val

    def run(self):
        while True:
            self.event.wait()
            tic = time.time()
            self.alphabeta(self.__src_board,
                           depth=0,
                           isMaximizingPlayer=True,
                           alpha=-float('inf'),
                           beta=float('inf'),
                           max_depth=self.__max_depth)
            print("Sending after {:.3f}s".format(time.time()-tic))
            self.__send_mov([self.__best_move.parse_for_socket()])

    def set_send_mov(self, send_mov_func):
        self.__send_mov = send_mov_func

