class GamePlay:

    def __init__(self, player1, player2, game):
        self.players = [player1, player2]
        self.game = game
        self.history = []

    def playRound(self):
        actions = tuple(player.getStrategy() for player in self.players)
        round_payoffs = self.returnPlayerPayoffs(*actions)
        for player, payoff in zip(self.players, round_payoffs):
            player.addPayoff(payoff)
        self.addRoundToHistory(actions, round_payoffs)

    def playMultipleRounds(self, num_rounds):
        for i in range(num_rounds - 1):
            self.playRound()

    def returnPlayerPayoffs(self, action1, action2):
        return (self.game.getPayoff()[action1, action2],
                self.game.getPayoff()[action2, action1])

    def addRoundToHistory(self, actions, payoffs):
        return self.history.append([actions, payoffs])

    def getHistory(self):
        return self.history
