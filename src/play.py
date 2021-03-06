#!/usr/bin/python
# !/usr/bin/env python

# necessary packages
from mancala import *
from player import *
import argparse

if __name__ == '__main__':
    # commandline arguments
    # ./play player1 player2: random, minimax, alphabeta, human
    # ./play random human: random VS you

    player_choices = ['random', 'minimax', 'alphabeta', 'human']
    # ############### Argparse ###############
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("player1",
                        type=str,
                        help="role of player 1",
                        choices=player_choices,
                        default='random')
    parser.add_argument("player2",
                        type=str,
                        help="role of player 2",
                        choices=player_choices,
                        default='human')
    parser.add_argument("-d1",
                        "--depth1",
                        type=int,
                        help="maximum depth of player1",
                        default=6)
    parser.add_argument("-d2",
                        "--depth2",
                        type=int,
                        help="maximum depth of ",
                        default=6)

    args = parser.parse_args()

    player1 = Player(1, args.player1, args.depth1)
    player2 = Player(2, args.player2, args.depth2)

    mgame = Mancala()

    mgame.play_game(player1, player2)
