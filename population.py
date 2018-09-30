import numpy as np


class Population:

    def __init__(self, players):
        self.players = players

    def pairTwoRndPlayers(self):
        return np.random.choice(self.players,
                                size=2,
                                replace=False)
        # return [Player(0), Player(0)]
