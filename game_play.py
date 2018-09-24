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
        print("Game history: {} \n\n {} \n\n {}".format(
            self.history, self.players[0], self.players[1]))

    def returnPlayerPayoffs(self, action1, action2):
        return (self.game.getPayoff()[action1, action2],
                self.game.getPayoff()[action2, action1])

    def addRoundToHistory(self, actions, payoffs):
        return self.history.append([actions, payoffs])
