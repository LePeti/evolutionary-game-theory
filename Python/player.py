import numpy as np


class Player:

    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff_history = []

    def getStrategy(self):
        return self.strategy

    def getPayoffHistory(self):
        return self.payoff_history

    def addPayoffToHistory(self, payoff):
        self.payoff_history.append(payoff)

    def getAveragePayoff(self):
        return np.mean(self.payoff_history)

    def __str__(self):
        return ("Player [{}] "
                "Average payoff: {}").format(
            self.getStrategy(),
            self.getAveragePayoff())
