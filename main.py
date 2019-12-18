from Python.player import Player
from Python.game import Game
from Python.game_play import GamePlay

import numpy as np

if __name__ == "__main__":
    np.random.seed(999)

    pd = Game(np.array([[2, 0],
                        [4, 1]]))
    players = [Player([[1, 0, 0]]) for _ in range(30)]

    num_generations = 5
    num_pairing = 5
    num_rounds = 20
    probability_of_mutation = 0.5

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

    relativeStratSuccess = gamePlay.calc_relative_strat_success_for_generation(
    )
    relativeStratSuccess.to_csv(
        f'output/num_gen_{num_generations}_'
        f'num_pairing_{num_pairing}_'
        f'num_rounds_{num_rounds}_'
        f'mute_prob_{probability_of_mutation}.csv',
        index=False
    )
