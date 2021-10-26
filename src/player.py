from math import floor, ceil
from random import choice
from copy import deepcopy


class Player(object):
    def __init__(self, index, algo, maximum_depth=float("inf"), depth=0):
        """Init a player

        ---
        index: 1/2 -> palyer1/2
        algo: the pattern of the player human/random/...
        ---

        """
        self.index = index
        self.opp_index = 3 - self.index  # the opposite index
        self.algo = algo
        self.depth = depth
        self.maximum_depth = maximum_depth

    def reset(self):
        """reset the player"""
        self.depth = 0

    def get_move(self, game):
        """get the move with a certian player"""
        algos_dict = {
            'human': self.human_player,
            'random': self.random_player,
            'minimax': self.minmax_player,
            'alphabeta': self.abpruning_player
        }
        return algos_dict[self.algo](game)

    def ask4move(self, game):
        """for human player, ask and return a move

        ---
        return move"""
        request_str = ""  # "Your turn:\n"

        if self.index == 1:
            request_str += f"\t{'-' * floor(7 * (game.M + 1) / 2)}Player1{'-' * ceil(7 * (game.M + 1) / 2)}\n"
            request_str += (f"\tLocation:   " +
                            " ||   ".join(map(str, range(1, 1 + game.M))) +
                            f" | -    \n")
            request_str += (f"\tNum pits:   " +
                            " ||   ".join(map(str, game.p1_pits())) +
                            f" | -   {game.p1_store()}\n")
        else:
            request_str += (f"\tLocation: -    |   " +
                            " ||   ".join(map(str, range(game.M, 0, -1))) +
                            f"\n")
            request_str += (f"\tNum pits: -   {game.p2_store()}|   " +
                            " ||   ".join(map(str, game.p2_pits()[::-1])) +
                            f"\n")
            request_str += f"\t{'-' * floor(7 * (game.M + 1) / 2)}Player2{'-' * ceil(7 * (game.M + 1) / 2)}\n"

        print(request_str)

        try:
            move = int(input('\tPlease enter your target pit:'))
        except:
            move = int(input('\tWrong input. Please try again:'))
        return move - 1

    def human_player(self, game):
        """human player"""
        move = self.ask4move(game)
        while not game.check_illegal_move(self, move):
            move = self.ask4move(game)
        return move

    def random_player(self, game):
        """random player"""
        legal_actions = game.filter_actions(self)
        move = choice(legal_actions)
        return move

    def score(self, game, h_choice=0):
        """calculate the current score of self player"""
        win_index, p1_score, p2_score = game.find_winner_scores()
        if game.check_end_game():
            if h_choice == 0:
                if win_index == self.index:
                    return 50
                elif win_index == self.opp_index:
                    return -50
                else:
                    return 0
            elif h_choice == 1:  # depth consider
                if win_index == self.index:
                    return 50 - self.depth
                elif win_index == self.opp_index:
                    return self.depth - 50
                else:
                    return 0
                pass
            elif h_choice == 2:  # diff consider
                if win_index == self.index:
                    return abs(p1_score - p2_score)
                elif win_index == self.opp_index:
                    return -abs(p1_score - p2_score)
                else:
                    return 0
            elif h_choice == 3:  # all consider
                if win_index == self.index:
                    return abs(p1_score - p2_score) - self.depth
                elif win_index == self.opp_index:
                    return -abs(p1_score - p2_score) + self.depth
                else:
                    return 0
            else:
                pass
        if win_index == self.index:
            return abs(p1_score - p2_score)
        elif win_index == self.opp_index:
            return -abs(p1_score - p2_score)
        else:
            return 0

    def reach_max_depth(self):
        """check whether it reachs the maximun depth"""
        return self.depth >= self.maximum_depth

    def max_value(self, game, ab_flag=False, alpha=float("-inf"), beta=float("inf")):
        """Find the max value for the next move"""
        if game.check_end_game() or self.reach_max_depth():
            return self.score(game), None
        v = float("-inf")
        move = -1
        for a in game.filter_actions(self):
            opp_player = Player(self.opp_index, self.algo, self.maximum_depth, self.depth + 1)

            next_game = deepcopy(game)
            next_game.sowing(self, a)

            v2, _ = opp_player.min_value(next_game, ab_flag, alpha, beta)
            if v2 > v:
                v = v2
                move = a
                alpha = max(alpha, v)
            if ab_flag and v >= beta:
                return v, move
        return v, move

    def min_value(self, game, ab_flag=False, alpha=float("-inf"), beta=float("inf")):
        """Find the min value for the next move"""
        if game.check_end_game() or self.reach_max_depth():
            return self.score(game), None
        v = float("inf")
        move = -1
        for a in game.filter_actions(self):
            opp_player = Player(self.opp_index, self.algo, self.maximum_depth, self.depth + 1)

            next_game = deepcopy(game)
            next_game.sowing(self, a)

            v2, _ = opp_player.max_value(next_game, ab_flag, alpha, beta)

            if v2 < v:
                v = v2
                move = a
                beta = min(beta, v)
            if ab_flag and v <= alpha:
                return v, move
        return v, move

    def minmax_player(self, game):
        """minmax player"""
        move = self.max_value(game)[1]
        return move

    def abpruning_player(self, game):
        """alpha-beta pruning player"""
        move = self.max_value(game, True)[1]
        return move
