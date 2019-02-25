# -*- coding: utf-8 -*-

"""
Source : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
Fourni un pseudo code et une explication extensive que j'ai utilisé pour ecrire le code
"""
from board_generator import BoardGenerator
from threading import Thread
import time


class IA(Thread):
    def __init__(self, src_board, max_depth=2):
        Thread.__init__(self)
        self.__src_board = src_board
        self.__best_move = None
        self.__generator = BoardGenerator(src_board)
        self.__send_mov = None
        self.__max_depth = max_depth

        self.event = None  # TODO: better event handling to allow for calculation during opponent turn

    def alphabeta(self, src_board, depth=0, isMaximizingPlayer=True, alpha=-float('inf'), beta=float('inf'), max_depth=5):
        """
        Parcours du graphe en alphabeta pour choisir le bestmove
        :param src_board:
        :param depth:
        :param isMaximizingPlayer:
        :param alpha:
        :param beta:
        :param max_depth:
        :return:
        """
        if src_board.win == 1: #on arrête si on a gagné
            return float('inf')

        if src_board.win == -1: #on arrête si on a perdu aussi
            return -float('inf')

        if depth == max_depth:
            return src_board.heuristic()

        if isMaximizingPlayer:
            best_val = -float('inf')
            for (board, move) in self.__generator.get_all_possible_boards():
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
            for (board, move) in self.__generator.get_all_possible_boards():
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
            self.alphabeta(self.__src_board, 0, True, -float('inf'), float('inf'), self.__max_depth,)
            print("Sending after {:.3f}s".format(time.time()-tic))
            self.__send_mov([self.__best_move.parse_for_socket()])

    def set_send_mov(self, send_mov_func):
        self.__send_mov = send_mov_func
