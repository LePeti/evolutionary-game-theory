import numpy as np


class GamePlay:
    """
    Definitions:
    - Game:           two players play the game once
    - Iterated game:  a game played for multiple rounds
    - Iteration:      whole population plays the iterated game multiple times
    """

    def __init__(self, population, game):
        self.population = population
        self.game = game
        self.history = []

    def playGame(self, num_rounds, num_games):
        pass

    def playRound(self, selectedPlayers):
        actions = tuple(player.getStrategy() for player in selectedPlayers)
        round_payoffs = self.getPlayerPayoffs(*actions)
        for player, payoff in zip(selectedPlayers, round_payoffs):
            player.addPayoffToHistory(payoff)
        self.addRoundToHistory(actions, round_payoffs)

    def playMultipleRounds(self, selectedPlayers, num_rounds=100):
        for _ in range(num_rounds - 1):
            self.playRound(selectedPlayers)

    def getPlayerPayoffs(self, player1_action, player2_action):
        return (int(self.game.getPayoff()[player1_action, player2_action]),
                int(self.game.getPayoff()[player2_action, player1_action]))

    def addRoundToHistory(self, actions, payoffs):
        return self.history.append([actions, payoffs])

    def getHistory(self):
        return self.history

    def pairUpPopulation(self):
        np.random.shuffle(self.population)
        return list(zip(self.population[::2], self.population[1::2]))
