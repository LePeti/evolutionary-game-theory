class Player:

    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff = []

    def getStrategy(self):
        return self.strategy

    def getPayoff(self):
        return self.payoff

    def addPayoff(self, payoff):
        self.getPayoff().append(payoff)

    def __str__(self):
        return "Player [{}] \n Payoff: {}".format(self.getStrategy(),
                                                  self.getPayoff())
