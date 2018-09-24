class Strategy(object):

    def __init__(self, default_strat=[['D', 0, 0]]):
        self.strategy = default_strat

        self.strat_nr = self.get_state_nr()

        self.current_state = 0

        self.payoff = []

        self.actions = []

    def add_state(self, state, transitions):
        self.strategy.append([state] + transitions)

        return self.strategy

    def remove_state(self, state_index, transition_reordering):
        del self.strategy[state_index]

        for state_ind, state in enumerate(self.strategy):
            for elem_ind, elem in enumerate(state):

                if elem == state_index:
                    self.strategy[state_ind][elem_ind] = \
                        transition_reordering.pop(0)

                else:
                    if elem > state_index and type(elem) == int:
                        self.strategy[state_ind][elem_ind] -= 1

        return self.strategy

    def change_transition(self,
                          state_index_from,
                          transition_ind,
                          state_index_to):
        self.strategy[state_index_from][transition_ind + 1] = state_index_to

        return self.strategy

    def change_state(self, state_ind):
        if self.strategy[state_ind][0] == 'C':
            self.strategy[state_ind][0] = 'D'
        else:
            self.strategy[state_ind][0] = 'C'

        return self.strategy

    def change_current_state(self, opponent_last_move):
        if not opponent_last_move:
            pass
        elif opponent_last_move == 'C':
            self.current_state = self.strategy[self.current_state][1]
        elif opponent_last_move == 'D':
            self.current_state = self.strategy[self.current_state][2]
        else:
            raise ValueError(
                'Opponent\'s last move should be either \'C\' \
                 or \'D\', however it is ',
                opponent_last_move)

        return self.current_state

    def get_current_state(self):
        return self.current_state

    def get_strategy(self):
        return self.strategy

    def get_state_nr(self):
        return len(self.strategy)


class Game(object):

    def __init__(self, payoffs):
        self.payoffs = payoffs

    def get_game(self):
        return self.payoffs

    def __str__(self):
        return str(self.get_game())


class Population(object):
    def __init__(self, nr_pop, default_strat=['D', 0, 0]):
        self.population = \
            [Strategy(default_strat=default_strat) for i in range(nr_pop)]

    def get_pop(self):
        return self.population

    def __str__(self):
        return str([x for strat in self.population for x in strat.strategy])


class Play_game(object):
    def __init__(self, strats, game, nr_iters):

        self.strats = strats

        self.game = game

    def play_round(self):
        for strat in self.strats:
            strat.actions += strat.strategy[strat.current_state][0]

        self.strats[0].change_current_state(self.strats[1].actions[-1])
        self.strats[1].change_current_state(self.strats[0].actions[-1])


strat1 = Strategy(default_strat=[['C', 0, 1], ['D', 0, 1]])
strat2 = Strategy()
game = Game([[2, 0], [3, 1]])
iters = 10
myFirstGame = Play_game([strat1, strat2], game, iters)

myFirstGame.strats[0].get_current_state()
myFirstGame.play_round()
print myFirstGame.strats[0].actions, myFirstGame.strats[1].actions

a = [[1, 2], [3, 4]]
a[-1][0]

myFirstPop = Population(nr_pop=10)
print myFirstPop

myFirstGame = Game([[2, 0], [3, 1]])
myFirstGame.payoffs[1][1]

a = []

myFirstGame = Game([[2, 0], [3, 1]])
myFirstGame

print myFirstGame

myFirstStrat = Strategy()

type(myFirstStrat)

print myFirstStrat.get_strategy()
print myFirstStrat.get_state_nr()
myFirstStrat.add_state('C', [1, 0])
myFirstStrat.add_state('C', [1, 2])
myFirstStrat.change_transition(0, 0, 1)
myFirstStrat.change_state(0)
myFirstStrat.remove_state(0, [0])
