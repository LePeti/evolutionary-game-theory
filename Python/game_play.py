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

    def __init__(self, population, game,
                 num_generations=10, num_pairing=5, num_rounds=100):
        self.population = population
        self.game = game
        self.game_history = pd.DataFrame()
        self.num_generations = num_generations
        self.num_pairing = num_pairing
        self.num_rounds = num_rounds

    def play_game_for_multiple_pairings(self, ith_generation):
        for ith_pairing in range(self.num_pairing):
            print(f'pairing: {ith_pairing}')
            self.playMultipleRoundsInPairs(
                ith_generation, ith_pairing, self.num_rounds)

    def playMultipleRoundsInPairs(self, ith_generation, ith_pairing,
                                  num_rounds):
        for ith_pair, pair in enumerate(self.pairUpPopulation()):
            print(f'pair: {ith_pair}')
            self.playMultipleRounds(
                *pair, ith_generation, ith_pairing, ith_pair, num_rounds)

    def playMultipleRounds(self, player1, player2,
                           ith_generation, ith_pairing, ith_pair, num_rounds):
        for i in range(num_rounds):
            self.playRound(player1, player2,
                           ith_generation, ith_pairing, ith_pair, i)

    def playRound(self, player1, player2,
                  ith_generation, ith_pairing, ith_pair, ith_round):
        player1_action = player1.getCurrentAction(player2.getLastAction())
        player2_action = player2.getCurrentAction(player1.getLastAction())
        player1_payoff = self.getRowPlayersPayoffs(
            player1_action, player2_action)
        player2_payoff = self.getRowPlayersPayoffs(
            player2_action, player1_action)
        player1.addPayoffToHistory(player1_payoff)
        player2.addPayoffToHistory(player2_payoff)
        self.addRoundToGameHistory(
            id(player1), ith_generation, ith_pairing, ith_pair, ith_round,
            player1.strategy, player1_action, player1_payoff, id(player2)
        )
        self.addRoundToGameHistory(
            id(player2), ith_generation, ith_pairing, ith_pair, ith_round,
            player2.strategy, player2_action, player2_payoff, id(player1)
        )

    def getRowPlayersPayoffs(self, player1_action, player2_action):
        return int(self.game.payoffTable[player1_action, player2_action])

    def addRoundToGameHistory(self, player_id,
                              ith_generation, ith_pairing, ith_pair, ith_round,
                              strat, action, payoff, opponents_id):
        self.game_history = self.game_history.append(
            {
                'player_id': player_id,
                'ith_generation': ith_generation, 'ith_pairing': ith_pairing,
                'ith_pair': ith_pair, 'ith_round': ith_round,
                'strategy': strat,
                'action': action, 'payoff': payoff,
                'opponents_id': opponents_id
            }, ignore_index=True
        )

    def pairUpPopulation(self):
        np.random.shuffle(self.population)
        return list(zip(self.population[::2], self.population[1::2]))

    def calc_relative_strat_success_for_generation(self, ith_generation=None):
        if ith_generation is not None:
            ith_generation_game_history = self.game_history[
                self.game_history['ith_generation'] == ith_generation
            ].copy()
        else:
            ith_generation_game_history = self.game_history.copy()

        payoff_total = ith_generation_game_history[['payoff']].sum()[0]
        ith_generation_game_history['tuple_strat'] = \
            ith_generation_game_history['strategy'].apply(self._listToTuple)
        stratPayoff = ith_generation_game_history[
            ['ith_generation', 'player_id', 'payoff', 'tuple_strat']
        ].groupby(['ith_generation', 'player_id', 'tuple_strat']).sum(
            ).reset_index()
        stratPayoff['relativePayoff'] = \
            stratPayoff[['payoff']] / payoff_total
        stratPayoff['strategy'] = \
            stratPayoff['tuple_strat'].apply(self._tupleToList)
        return stratPayoff

    def reproduce_population(self, ith_generation):
        relative_strat_success = \
            self.calc_relative_strat_success_for_generation(ith_generation)
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
