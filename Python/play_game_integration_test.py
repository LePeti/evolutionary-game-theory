from Python.player import Player
from Python.game import Game
from Python.game_play import GamePlay

import numpy as np


np.random.seed(999)

pd = Game(np.array([[2, 0],
                    [4, 1]]))
players = [Player([[1, 0, 0]], [[1, 0, 0]]) for _ in range(2)]

num_generations = 2
num_pairing = 1
num_rounds = 2
probability_of_mutation = 1

gamePlay = GamePlay(players, pd, num_pairing, num_rounds)

for ith_generation in range(num_generations):
    gamePlay.play_game_for_multiple_pairings(ith_generation)
    gamePlay.reproduce_population(ith_generation)
    gamePlay.mutate_population_with_prob(p=probability_of_mutation)
    gen_history = gamePlay.game_history[
        gamePlay.game_history['ith_generation'] == ith_generation]
    print(
        f'{ith_generation + 1}. generation avg payoff: '
        f'{gen_history["action"].mean()}'
    )

relativeStratSuccess = gamePlay.calc_relative_strat_success_for_generation()
