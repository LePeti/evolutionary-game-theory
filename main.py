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

    num_generations = 2
    num_pairing = 2
    num_rounds = 2

    gamePlay = GamePlay(players, pd, num_generations, num_pairing, num_rounds)

    for ith_generation in range(gamePlay.num_generations):
        gamePlay.play_game_for_multiple_pairings(ith_generation)
        gamePlay.reproduce_population(ith_generation)
        gamePlay.mutate_population_with_prob(p=0.2)

    relativeStratSuccess = gamePlay.calc_relative_strat_success_for_generation(
    )
    print(relativeStratSuccess.sort_values('relativePayoff', ascending=False))
