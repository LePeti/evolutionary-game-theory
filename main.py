from Python.player import *
from Python.game import *
from Python.game_play import *

import numpy as np

if __name__ == "__main__":
    np.random.seed(999)

    pd = Game(np.array([[2, 0],
                        [4, 1]]))
    players = \
        [Player([[1, 0, 0]]) for _ in range(4)] + \
        [Player([[0, 0, 0]]) for _ in range(4)] + \
        [Player([[0, 0, 1], [1, 0, 1]]) for _ in range(4)]

    num_pairing = 2
    gamePlay = GamePlay(players, pd)

    # Play the game
    for generation in range(2):
        for ith_pairing in range(num_pairing):
            print(f'pairing: {ith_pairing}')
            gamePlay.playMultipleRoundsInPairs(
                ith_pairing=ith_pairing, num_rounds=20)

        gamePlay.reproduce_population()
        gamePlay.mutate_population_with_prob(p=0.2)

    relativeStratSuccess = gamePlay.calcRelativeStratSuccess()
    print(relativeStratSuccess.sort_values(
        'relativePayoff', ascending=False))
