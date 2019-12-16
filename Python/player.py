import numpy as np


class Player:

    '''
    A player is basically a strategy. A strategy is a finite state
    automaton where nodes are actions and transitions point to nodes.
    Transitions are reactions to the opponent strategy's last action.
    An example strategy is Tit-for-tat: you start with 'cooperation'
    and then do what your opponent did last round. It's represented like so:

    [[0, 0, 1], [1, 0, 1]]

    The first string in each sublist is the action, the second element in
    the sublists is the transition which tells you to which state
    (node/sublist) to go when the opponent cooperated. 0 means go to the 0th
    node, i.e. stay at the current node if you are already there. The very
    first action is determined by the first element of the first node.
    '''

    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff_history = []
        self.state_index_history = []

    def get_current_action(self, opponents_last_action):
        if self.get_last_state_index() is None:
            self.update_state_index_history_with(0)
            return self.strategy[0][0]
        last_state = self.get_last_state()
        current_state_index = last_state[opponents_last_action + 1]
        current_action = self.strategy[current_state_index][0]
        self.update_state_index_history_with(current_state_index)
        return current_action

    def get_last_action(self):
        if self.get_last_state() is None:
            return self.strategy[0][0]
        else:
            return self.get_last_state()[0]

    def get_last_state_index(self):
        if not self.state_index_history:
            return None
        else:
            return self.state_index_history[-1]

    def get_last_state(self):
        if self.get_last_state_index() is None:
            return None
        else:
            return self.strategy[self.get_last_state_index()]

    def update_state_index_history_with(self, state_index):
        self.state_index_history.append(state_index)

    def add_payoff_to_history(self, payoff):
        self.payoff_history.append(payoff)

    def get_average_payoff(self):
        return np.mean(self.payoff_history)

    def randomly_mutate_strategy(self):
        random_mutation = np.random.choice([
            self.remove_state,
            self.add_new_state,
            self.rewire_random_transition,
            self.change_random_state_action
        ])

        print(random_mutation.__name__)

        try:
            random_mutation()
        except Exception as Error:
            print(Error)
            self.randomly_mutate_strategy()

        return self.strategy

    def change_random_state_action(self):
        random_state_index = np.random.randint(len(self.strategy))
        self.strategy[random_state_index][0] = \
            self.strategy[random_state_index][0] * -1 + 1

    def rewire_random_transition(self):
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

    def add_new_state(self):
        self._construct_and_append_new_state()
        self._connect_rnd_not_last_state_with_last_state()

    def _construct_and_append_new_state(self):
        new_action = np.random.choice([0, 1])
        new_transitions = np.random.choice([0, 1], size=2)
        self.strategy.append([new_action] + list(new_transitions))

    def _connect_rnd_not_last_state_with_last_state(self):
        rnd_but_not_last_state_index = np.random.choice(len(self.strategy) - 1)
        rnd_transition_index = np.random.choice([1, 2])
        self.strategy[rnd_but_not_last_state_index][rnd_transition_index] = \
            len(self.strategy) - 1

    def remove_state(self):
        if len(self.strategy) == 1:
            raise Exception(
                f'Cannot remove state from single state strategy: '
                f'{self.strategy}')
        random_state_index = np.random.choice(range(len(self.strategy)))
        self.strategy.pop(random_state_index)

        self._rewire_transitions_pointing_to_removed_state()

    def _rewire_transitions_pointing_to_removed_state(self):
        available_states = range(len(self.strategy))

        for state_index, state in enumerate(self.strategy):
            for transition_index, transition in enumerate(state[1:]):
                if transition not in available_states:
                    new_random_state_index = np.random.choice(available_states)
                    self.strategy[state_index][transition_index + 1] = \
                        new_random_state_index

    def __str__(self):
        return ("Player [{}] "
                "Average payoff: {}").format(
            self.strategy,
            self.get_average_payoff())
