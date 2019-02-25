# -*- coding: utf-8 -*-

"""
Source : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
Fourni un pseudo code et une explication extensive que j'ai utilisé pour ecrire le code
"""
from board_generator import BoardGenerator
import time


class IA:
    def __init__(self, src_board, socket):
        self.__src_board = src_board
        self.__best_move = None
        self.__generator = BoardGenerator(src_board)

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
            return float('inf'), None

        if src_board.win == -1: #on arrête si on a perdu aussi
            return -float('inf'), None

        if depth == max_depth:
            return src_board.heuristic(), None

        if isMaximizingPlayer:
            best_val = -float('inf')
            best_move = None
            for (board, move) in self.__generator.get_all_possible_boards():
                value = self.alphabeta(board, depth + 1, False, alpha, beta, max_depth)
                if best_val < value:
                    best_val = value
                    best_move = move
                    if depth == 0:
                        self.__best_move = best_move
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            return best_val, best_move

        else:
            best_val = float('inf')
            best_move = None
            for (board, move) in self.__generator.get_all_possible_boards():
                value = self.alphabeta(board, depth + 1, True, alpha, beta, max_depth)
                if best_val < value:
                    best_val = value
                    best_move = move
                    if depth == 0:
                        self.__best_move = best_move
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val, best_move

    def run(self, max_depth):
        self.alphabeta(self.__src_board, 0, True, -float('inf'), float('inf'), max_depth)
        # tic = time.time()
        # while time.time()-tic <= 2:
        #     continue
        self.__send_mov(self.__best_move.parse_for_socket())

    def set_send_mov(self, send_mov_func):
        self.__send_mov = send_mov_func

#Pour lancer le alphabeta sur un arbre il faut lancer la fonction

"""
prendre en compte le timing"""

#alphabeta(board_init, 0, True, -float('inf'), float('inf'),max_depth)
