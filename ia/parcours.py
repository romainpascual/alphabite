# -*- coding: utf-8 -*-

"""
Source : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
Fourni un pseudo code et une explication extensive que j'ai utilisé pour ecrire le code
"""
from board_generator import BoardGenerator

def alphabeta(src_board, depth=0, isMaximizingPlayer=True, alpha=-float('inf'), beta=float('inf'), max_depth=5):
    """
    Parcours du graphe en alphabeta pour choisir le bestmove
    :param board:
    :param depth:
    :param isMaximizingPlayer:
    :param alpha:
    :param beta:
    :param max_depth:
    :return: La best_val
    """
    generator = BoardGenerator(src_board)
    if src_board.isterminal() is True: #on arrete si on a gagner
        return src_board.heuristic()

    if depth == max_depth:
        return src_board.heuristic()

    if isMaximizingPlayer:
        best_val = -float('inf')
        best_move = None
        for (board, move) in generator.get_all_possible_boards():
            value = alphabeta(board, depth + 1, False, alpha, beta, max_depth)
            if best_val < value:
                best_val = value
                best_move = move
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val, best_move

    else:
        best_val = float('inf')
        best_move = None
        for (board, move) in generator.get_all_possible_boards():
            value = alphabeta(board, depth + 1, True, alpha, beta, max_depth)
            if best_val < value:
                best_val = value
                best_move = move
            #best_val = min(best_val, value)
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best_move

#Pour lancer le alphabeta sur un arbre il faut lancer la fonction

"""
board.nextmove ++ prendre en compte le timing"""

#alphabeta(board_init, 0, True, -float('inf'), float('inf'))