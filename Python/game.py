class Game:
    '''
    A Game is the payoff matrix of a game.
    E.g. for prisoner's dilemma it's

      C  D
    C[2, 0]
    D[4, 1]

    The payoffs are from the row player's point of view,
    where first action is 'cooperate' and second is 'defect'
    '''

    def __init__(self, payoffTable):
        self.payoffTable = payoffTable
