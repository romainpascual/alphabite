# -*- coding: utf-8 -*-

"""
Source : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
Fourni un pseudo code et une explication extensive que j'ai utilisé pour ecrire le code
"""


def alphabeta(node=0, depth=0, isMaximizingPlayer=True, alpha=-float('inf'), beta=float('inf')):

    if node.isterminal() is True:
        return heuristic(node)

    if isMaximizingPlayer:
        best_val = -float('inf')
        for node in node.children():
            value = alphabeta(node, depth + 1, False, alpha, beta)
            best_val = max(best_val, value)
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val

    else:
        best_val = float('inf')
        for node in node.children():
            value = alphabeta(node, depth + 1, True, alpha, beta)
            best_val = min(best_val, value)
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val

#Pour lancer le alphabeta sur un arbre il faut lancer la fonction

minimax(0, 0, true, -float('inf'), float('inf'))