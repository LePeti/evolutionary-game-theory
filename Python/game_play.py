import numpy as np
import pandas as pd
from tqdm import tqdm

from Python.player import Player


class GamePlay:
    """
    Parameters:
    - population: multiple `Player`s who will play the game
    - game: (Class `Game`) payoff matrix which determines the rules of the game
    - num_pairing: number of times the population is paired up to play
    - num_rounds: number of iterations one pair plays the game

    How many times is a single game played:
    num_generation x num_pairing x num_rounds

    General vocab:
    - Game:           two players play the game once
    - Iterated game:  a game played for `num_rounds` rounds
    - Iteration:      whole population plays the iterated game `num_pairing`
                      times
    - Generations:    after an Iteration, the population reproduces and the
                      next generation starts the next iteration
    """

    def __init__(self, population, game, num_pairing=5, num_rounds=100):
        self.population = population
        self.game = game
        self.game_history = pd.DataFrame()
        self.num_pairing = num_pairing
        self.num_rounds = num_rounds

    def play_game_for_multiple_pairings(self, ith_generation):
        for ith_pairing in tqdm(range(self.num_pairing)):
            self.play_multiple_rounds_in_pairs(
                ith_generation, ith_pairing, self.num_rounds)

    def play_multiple_rounds_in_pairs(self, ith_generation, ith_pairing,
                                      num_rounds):
        for ith_pair, pair in enumerate(self.pair_up_population()):
            self.play_multiple_rounds(
                *pair, ith_generation, ith_pairing, ith_pair, num_rounds)

    def play_multiple_rounds(self, player1, player2, ith_generation,
                             ith_pairing, ith_pair, num_rounds):
        for i in range(num_rounds):
            self.play_round(player1, player2,
                            ith_generation, ith_pairing, ith_pair, i)

    def play_round(self, player1, player2,
                   ith_generation, ith_pairing, ith_pair, ith_round):
        player1_action = player1.get_current_action(player2.get_last_action())
        player2_action = player2.get_current_action(player1.get_last_action())
        player1_payoff = self.get_row_players_payoffs(
            player1_action, player2_action)
        player2_payoff = self.get_row_players_payoffs(
            player2_action, player1_action)
        player1.add_payoff_to_history(player1_payoff)
        player2.add_payoff_to_history(player2_payoff)
        self.add_round_to_game_history(
            id(player1), ith_generation, ith_pairing, ith_pair, ith_round,
            player1.strategy, player1.original_strategy, player1_action,
            player1_payoff, id(player2)
        )
        self.add_round_to_game_history(
            id(player2), ith_generation, ith_pairing, ith_pair, ith_round,
            player2.strategy, player2.original_strategy, player2_action,
            player2_payoff, id(player1)
        )

    def get_row_players_payoffs(self, player1_action, player2_action):
        return int(self.game.payoffTable[player1_action, player2_action])

    def add_round_to_game_history(self, player_id, ith_generation, ith_pairing,
                                  ith_pair, ith_round,
                                  strat, orig_strat, action, payoff,
                                  opponents_id):
        self.game_history = self.game_history.append(
            {
                'player_id': player_id,
                'ith_generation': ith_generation, 'ith_pairing': ith_pairing,
                'ith_pair': ith_pair, 'ith_round': ith_round,
                'strategy': strat,
                'orig_strat': orig_strat,
                'action': action, 'payoff': payoff,
                'opponents_id': opponents_id
            }, ignore_index=True
        )

    def pair_up_population(self):
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
            ith_generation_game_history['strategy'].apply(self._list_to_tuple)
        ith_generation_game_history['tuple_orig_strat'] = \
            ith_generation_game_history['orig_strat'].apply(
                self._list_to_tuple)
        grp_by_cols = ['ith_generation', 'player_id',
                       'tuple_strat', 'tuple_orig_strat']
        stratPayoff = ith_generation_game_history[grp_by_cols + ['payoff']] \
            .groupby(grp_by_cols).sum().reset_index()
        stratPayoff['relativePayoff'] = \
            stratPayoff[['payoff']] / payoff_total
        stratPayoff['strategy'] = \
            stratPayoff['tuple_strat'].apply(self._tuple_to_list)
        stratPayoff['orig_strat'] = \
            stratPayoff['tuple_orig_strat'].apply(self._tuple_to_list)
        return stratPayoff

    def reproduce_population(self, ith_generation):
        relative_strat_success = \
            self.calc_relative_strat_success_for_generation(ith_generation)
        population_size = len(relative_strat_success.index)

        new_population_strategies = np.random.choice(
            a=relative_strat_success['strategy'].values,
            p=relative_strat_success['relativePayoff'].values,
            size=population_size
        )
        self.population = [Player(strat, strat)
                           for strat in new_population_strategies]

    def mutate_population_with_prob(self, p):
        for player in self.population:
            if np.random.uniform() <= p:
                player.randomly_mutate_strategy()

    def _tuple_to_list(self, t):
        return list(map(self._tuple_to_list, t)) if isinstance(t, tuple) else t

    def _list_to_tuple(self, l):
        return tuple(map(self._list_to_tuple, l)) if isinstance(l, list) else l
