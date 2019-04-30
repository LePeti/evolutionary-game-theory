import numpy as np


class Player:

    '''
    A player is basically a strategy. A strategy is a finite state
    automaton where nodes are actions and transitions point to nodes.
    Transitions are reactions to the opponent strategy's last action.
    An example strategy is Tit-for-tat: you start with 'cooperation'
    and then do what your opponent did last round. It's represented like so:

    [['C', 0, 1], ['D', 0, 1]]

    The first string in the tuple is the action, the second element in
    the tuple is the transition which tells you to which state (node)
    to go when the opponent cooperated. 0 means go to the 0th node,
    i.e. stay at the current node if you are already there.
    '''

    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff_history = []

    def getStrategy(self):
        return self.strategy

    def getCurrentAction(self, last_action_index, opponents_action):
        last_action_node = self.getStrategy()[last_action_index]
        current_action_index = last_action_node[opponents_action + 1]
        current_action = self.getStrategy()[current_action_index][0]
        return current_action

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
