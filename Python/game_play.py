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
        self.game_history = []

    def playGame(self, num_rounds, num_games):
        pass

    def playMultipleRounds(self, selectedPlayers, num_rounds=100):
        for _ in range(num_rounds - 1):
            self.playRound(selectedPlayers)

    def playRound(self, player1, player2):
        player1_action = player1.getCurrentAction(player2.getLastAction())
        player2_action = player2.getCurrentAction(player1.getLastAction())
        player1_payoff = self.getRowPlayersPayoffs(
            player1_action, player2_action)
        player2_payoff = self.getRowPlayersPayoffs(
            player2_action, player1_action)
        player1.addPayoffToHistory(player1_payoff)
        player2.addPayoffToHistory(player2_payoff)
        self.addRoundToGameHistory(
            player1_action, player2_action, player1_payoff, player2_payoff)

    def getRowPlayersPayoffs(self, player1_action, player2_action):
        return int(self.game.payoffTable[player1_action, player2_action])

    def addRoundToGameHistory(self, player1_action, player2_action,
                              player1_payoff, player2_payoff):
        return self.game_history.append(
            {
                'p1_payoff': player1_payoff, 'p2_payoff': player2_payoff,
                'p1_action': player1_action, 'p2_action': player2_action,
            }
        )

    def pairUpPopulation(self):
        np.random.shuffle(self.population)
        return list(zip(self.population[::2], self.population[1::2]))
