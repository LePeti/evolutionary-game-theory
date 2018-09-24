from player import *
from game import *
from game_play import *

import numpy as np

if __name__ == "__main__":
    p1 = Player(0)
    p2 = Player(1)
    pd = Game(np.array([[2, 0], [4, 1]]))
    pd_game = GamePlay(p1, p2, pd)

    pd_game.playRound()
    pd_game.playRound()
    pd_game.playRound()
