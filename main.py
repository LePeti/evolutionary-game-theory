from Python.player import *
from Python.game import *
from Python.game_play import *

import numpy as np

if __name__ == "__main__":
    np.random.seed(999)

    pd = Game(np.array([[2, 0],
                        [4, 1]]))
    players = [Player([[1, 0, 0]]) for _ in range(100)]
    gamePlay = GamePlay(players, pd)

    # Play the game
    for i in range(100):
        print(f'pairing: {i}')
        gamePlay.playMultipleRoundsInPairs(100)

    # Reproduce

    # Mutate

    # Play again

    players_sorted_by_strat = sorted(
        players, key=lambda player: player.strategy
    )
    for player in players_sorted_by_strat:
        print(player)
