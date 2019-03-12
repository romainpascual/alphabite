# -*- coding: utf-8 -*-

"""
Source : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
Fourni un pseudo code et une explication extensive que j'ai utilisé pour ecrire le code
"""
from board_generator import BoardGenerator
from threading import Thread
import time
from threading import Timer

SURE_WIN = 100000


class IA(Thread):
    def __init__(self, src_board, max_depth=6):
        Thread.__init__(self)
        self.__src_board = src_board
        self.__best_move = None
        self.__send_mov = None
        self.__max_depth = max_depth
        self.__my_species = None
        self.__enemy_species = None

        self.__hasTimedOut = False
        self.__shouldRun = True

        self.event = None  # TODO: better event handling to allow for calculation during opponent turn

    def set_species(self, species):
        self.__my_species = species
        self.__enemy_species = 'v' if self.__my_species == 'w' else 'w'

    def alphabeta(self,
                  src_board,
                  depth=0,
                  our_prev_move=None,
                  their_prev_move = None,
                  is_maximizing_player=True,
                  alpha=-float('inf'),
                  beta=float('inf'),
                  max_depth=6,
                  certitude=True):
        """
        Alphabeta AI to choose the best move to play. The best move is stored in self.__best_move
        :param src_board: Actual Board on which we apply Alphabeta
        :param depth: Actual depth of the graph
        :param our_prev_move: Our previous move (equals None if previous move has changed our population)
        :param their_prev_move: Enemy previous move (equals None if previous move has changed their population)
        :param is_maximizing_player: True if max layer of the minimax and False otherwise
        :param alpha: actual value of alpha in the alphabeta propagation
        :param beta: actual value of beta in the alphabeta propagation
        :param max_depth: Max propagation depth in graph
        :param certitude: Indicates if the current branch is child of a probability
        :return: best_value, victory (values for algorithm sake only)
        """
        victory = 0
        best_board = None

        if depth == max_depth or src_board.is_winning_position:
            return src_board.heuristic(self.__my_species)

        if is_maximizing_player:
            current_species = self.__my_species
            prev_move = our_prev_move
            best_val = float('-inf')

        else:
            current_species = self.__enemy_species
            prev_move = their_prev_move
            best_val = float('inf')

        generator = BoardGenerator(src_board, current_species, prev_move)

        # Exploring all possible move at this level
        for (board, p), move in generator.get_all_possible_boards():
            # Returning a dummy value if timing out to close all branch exploration
            if self.__hasTimedOut:
                return float('-inf'), 0

            # Setting a fallback value in case of time_out
            if depth == 0 and self.__best_move is None:
                self.__best_move = move
                best_board = board

            # Setting the certitude of the branch to false if the probability is less than 1
            if p != 1:
                certitude = False

            # If the population of the current species has changed with the move, allow for turn-around next turn
            if src_board.get_species_population(current_species) ==\
                    board.get_species_population(current_species):
                if current_species == self.__my_species:
                    our_prev_move = move
                else:
                    their_prev_move = move
            else:
                if current_species == self.__my_species:
                    our_prev_move = None
                else:
                    their_prev_move = None

            # Recursive alphabeta
            value, victory = self.alphabeta(board,
                                            depth=depth + 1,
                                            our_prev_move= our_prev_move,
                                            their_prev_move=their_prev_move,
                                            is_maximizing_player= not is_maximizing_player,
                                            alpha=alpha,
                                            beta=beta,
                                            max_depth=max_depth,
                                            certitude=certitude)

            # If the branch leads to a sure win/loss, give a huge value to the best_value
            # This is only possible at the node directly before the win/loss
            if certitude and victory == 1:
                value = SURE_WIN
            elif certitude and victory == -1:
                value = -SURE_WIN
            else:
                value *= p

            # If origin of the decision tree, print all possible moves and their attributes
            if depth == 0:
                print(move, value, p)

            # Here we have to segregate the cases depending on the Min or Max status of the current node
            # Max node
            if is_maximizing_player:
                # If we are at the origin node (only possible for Max player), we have to handle things differently
                #  - allow for best move update
                #  - select the most promising branch if alpha beta raises an equality
                if depth == 0:
                    # If the value is greater than the current best value, update best_value, best_move and best_board
                    if best_val < value:
                        best_val = value
                        self.__best_move = move
                        best_board = board
                    # If the algorithm encounters an equality, we'll select the board that has the best heuristic
                    elif best_val == value and p == 1\
                            and best_board.heuristic(self.__my_species)[0] < board.heuristic(self.__my_species)[0]:
                        self.__best_move = move
                        best_board = board
                # Deep nodes handling
                elif best_val < value:
                    best_val = value
                if beta <= best_val:
                    return best_val, 0
                alpha = max(alpha, best_val)

            # Min node
            else:
                if value < best_val:
                    best_val = value
                if best_val <= alpha:
                    return best_val, 0
                beta = min(beta, best_val)

        return best_val, 0

    def turn_off(self):
        self.__shouldRun = False
        t = 4
        while t:
            print('Turning off IA in {} seconds.'.format(t), end='\r')
            time.sleep(1)
            t -= 1

    def timeout_handler(self):
        print("Timeout... Sending non-optimal best move")
        self.__send_mov([self.__best_move.parse_for_socket()])
        self.__hasTimedOut = True
        self.__best_move = None

    def run(self):
        while self.__shouldRun:
            if self.event.wait(4.):
                self.__hasTimedOut = False
                tic = time.time()
                timer = Timer(2, self.timeout_handler)
                timer.start()
                best_val = self.alphabeta(self.__src_board,
                                          depth=0,
                                          our_prev_move=None,
                                          their_prev_move=None,
                                          is_maximizing_player=True,
                                          alpha=-float('inf'),
                                          beta=float('inf'),
                                          max_depth=self.__max_depth)
                timer.cancel()
                if not self.__hasTimedOut:
                    print("Sending after {:.3f}s. Best val is {}".format(time.time()-tic, best_val))
                    self.__send_mov([self.__best_move.parse_for_socket()])
                self.__best_move = None
        print('IA is shutdown.', ' '*20)

    def set_send_mov(self, send_mov_func):
        self.__send_mov = send_mov_func
