from mancala import *
from player import *




player1 = Player(1, 'alphabeta',8)  # 'human' 'minmax', 6

player2 = Player(2, 'random')
# player2 = Player(2, 'human')
# player2 = Player(2, 'minmax',5)
mgame = Mancala()

mgame.play_game(player1, player2)