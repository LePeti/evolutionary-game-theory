import numpy as np
import pandas as pd
from Python.player import Player


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
        self.game_history = pd.DataFrame()

    def playMultipleRoundsInPairs(self, ith_pairing, num_rounds=100):
        for ith_pair, pair in enumerate(self.pairUpPopulation()):
            print(f'pair: {ith_pair}')
            self.playMultipleRounds(*pair, ith_pair, ith_pairing, num_rounds)

    def playMultipleRounds(self, player1, player2, ith_pair, ith_pairing,
                           num_rounds=100):
        for i in range(num_rounds):
            self.playRound(player1, player2, ith_round=i, ith_pair=ith_pair,
                           ith_pairing=ith_pairing)

    def playRound(self, player1, player2, ith_round, ith_pair, ith_pairing):
        player1_action = player1.getCurrentAction(player2.getLastAction())
        player2_action = player2.getCurrentAction(player1.getLastAction())
        player1_payoff = self.getRowPlayersPayoffs(
            player1_action, player2_action)
        player2_payoff = self.getRowPlayersPayoffs(
            player2_action, player1_action)
        player1.addPayoffToHistory(player1_payoff)
        player2.addPayoffToHistory(player2_payoff)
        self.addRoundToGameHistory(
            id(player1), ith_round, ith_pair, ith_pairing,
            player1.strategy, player1_action, player1_payoff, id(player2)
        )
        self.addRoundToGameHistory(
            id(player2), ith_round, ith_pair, ith_pairing,
            player2.strategy, player2_action, player2_payoff, id(player1)
        )

    def getRowPlayersPayoffs(self, player1_action, player2_action):
        return int(self.game.payoffTable[player1_action, player2_action])

    def addRoundToGameHistory(self, player_id, ith_round, ith_pair, ith_pairing,
                              strat, action, payoff, opponents_id):
        self.game_history = self.game_history.append(
            {
                'player_id': player_id,
                'generation': None, 'ith_pairing': ith_pairing,
                'ith_pair': ith_pair, 'ith_round': ith_round,
                'strategy': strat,
                'action': action, 'payoff': payoff,
                'opponents_id': opponents_id
            }, ignore_index=True
        )

    def _convertNestedListToTuple(self, asdf):
        tuple(tuple(list_elem) for list_elem in asdf)

    def pairUpPopulation(self):
        np.random.shuffle(self.population)
        return list(zip(self.population[::2], self.population[1::2]))

    def calcRelativeStratSuccess(self):
        payoff_total = self.game_history[['payoff']].sum()[0]
        self.game_history['tuple_strat'] = \
            self.game_history['strategy'].apply(self._listToTuple)
        stratPayoff = self.game_history[
            ['player_id', 'payoff', 'tuple_strat']
        ].groupby(['player_id', 'tuple_strat']).sum().reset_index()
        stratPayoff['relativePayoff'] = \
            stratPayoff[['payoff']] / payoff_total
        stratPayoff['strategy'] = \
            stratPayoff['tuple_strat'].apply(self._tupleToList)
        return stratPayoff

    def reproduce_population(self):
        relative_strat_success = self.calcRelativeStratSuccess()
        population_size = len(relative_strat_success.index)

        new_population_srategies = np.random.choice(
            a=relative_strat_success['strategy'].values,
            p=relative_strat_success['relativePayoff'].values,
            size=population_size
        )
        self.population = [Player(strat) for strat in new_population_srategies]

    def mutate_population_with_prob(self, p):
        for player in self.population:
            if np.random.uniform() <= p:
                player.randomlyMutateStrategy()

    def _tupleToList(self, t):
        return list(map(self._tupleToList, t)) if isinstance(t, tuple) else t

    def _listToTuple(self, l):
        return tuple(map(self._listToTuple, l)) if isinstance(l, list) else l
