import numpy as np
from random import shuffle


class Population:

    def __init__(self, players):
        self.players = players

    def pairTwoRndPlayers(self):
        return np.random.choice(self.players,
                                size=2,
                                replace=False)

    def pairUpPopulation(self):
        shuffle(self.players)
        return list(zip(self.players[::2], self.players[1::2]))
