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
        self.state_index_history = []

    def getCurrentAction(self, opponents_last_action):
        if self.getLastStateIndex() is None:
            self.updateStateIndexHistoryWith(0)
            return self.strategy[0][0]
        last_state = self.getLastState()
        current_state_index = last_state[opponents_last_action + 1]
        current_action = self.strategy[current_state_index][0]
        self.updateStateIndexHistoryWith(current_state_index)
        return current_action

    def getLastAction(self):
        if self.getLastState() is None:
            return self.strategy[0][0]
        else:
            return self.getLastState()[0]

    def getLastStateIndex(self):
        if not self.state_index_history:
            return None
        else:
            return self.state_index_history[-1]

    def getLastState(self):
        if self.getLastStateIndex() is None:
            return None
        else:
            return self.strategy[self.getLastStateIndex()]

    def updateStateIndexHistoryWith(self, state_index):
        self.state_index_history.append(state_index)

    def addPayoffToHistory(self, payoff):
        self.payoff_history.append(payoff)

    def getAveragePayoff(self):
        return np.mean(self.payoff_history)

    def changeRandomStateAction(self):
        random_state_index = np.random.randint(len(self.strategy))
        self.strategy[random_state_index][0] = \
            self.strategy[random_state_index][0] * -1 + 1

    def rewireRandomTransition(self):
        if len(self.strategy) == 1:
            raise Exception(
                f'Cannot rewire single state strategy ({self.strategy})'
            )
        state_indexes = list(range(len(self.strategy)))
        random_state_index = np.random.choice(state_indexes)
        random_transition_index = np.random.choice([1, 2])
        available_new_state_indexes = list(set(state_indexes) - set(
                [self.strategy[random_state_index][random_transition_index]])
        )
        new_random_state_index = np.random.choice(available_new_state_indexes)
        self.strategy[random_state_index][random_transition_index] = \
            new_random_state_index

    def addNewState(self):
        self._constructAndAppendNewState()
        self._connectRndNotLastStateWithLastState()

    def _constructAndAppendNewState(self):
        new_action = np.random.choice([0, 1])
        new_transitions = np.random.choice([0, 1], size=2)
        self.strategy.append([new_action] + list(new_transitions))

    def _connectRndNotLastStateWithLastState(self):
        rnd_but_not_last_state_index = np.random.choice(len(self.strategy) - 1)
        rnd_transition_index = np.random.choice([1, 2])
        self.strategy[rnd_but_not_last_state_index][rnd_transition_index] = \
            len(self.strategy) - 1

    def __str__(self):
        return ("Player [{}] "
                "Average payoff: {}").format(
            self.strategy,
            self.getAveragePayoff())
