import unittest
import numpy as np
from mock import patch

from Python.game_play import GamePlay
from Python.game import Game
from Python.player import Player


class TestGamePlay(unittest.TestCase):

    def setUp(self):
        self.pd = Game(np.array([[2, 0],
                                 [4, 1]]))
        self.players = [Player([[0, 0, 0]]), Player([[1, 0, 0]])]
        self.subject = GamePlay(population=self.players, game=self.pd)

    @patch('Python.player.Player.addPayoffToHistory')
    def test_playRound_callsaddPayoffToHistoryTwice(self, mock):
        self.subject.playRound(self.players[0], self.players[1],
                               ith_generation=None, ith_pairing=None,
                               ith_pair=None, ith_round=None)
        self.assertEqual(mock.call_count, 2)

    @patch('Python.game_play.GamePlay.addRoundToGameHistory')
    def test_playRound_callsaddRoundToGameHistoryWithCorrectParams(self, mock):
        ith_generation = None
        ith_pairing = None
        ith_pair = None
        ith_round = None

        self.subject.playRound(*self.players,
                               ith_generation=ith_generation,
                               ith_pairing=ith_pairing,
                               ith_pair=ith_pair, ith_round=ith_round)

        p1_strat = self.players[0].strategy
        p2_strat = self.players[1].strategy
        p1_action = self.players[0].strategy[0][0]
        p2_action = self.players[1].strategy[0][0]
        p1_payoff = self.subject.getRowPlayersPayoffs(p1_action, p2_action)
        p2_payoff = self.subject.getRowPlayersPayoffs(p2_action, p1_action)

        self.assertEqual(mock.call_args_list[0][0][0], id(self.players[0]))
        self.assertEqual(mock.call_args_list[0][0][1], ith_generation)
        self.assertEqual(mock.call_args_list[0][0][2], ith_pairing)
        self.assertEqual(mock.call_args_list[0][0][3], ith_pair)
        self.assertEqual(mock.call_args_list[0][0][4], ith_round)
        self.assertEqual(mock.call_args_list[0][0][5], p1_strat)
        self.assertEqual(mock.call_args_list[0][0][6], p1_action)
        self.assertEqual(mock.call_args_list[0][0][7], p1_payoff)
        self.assertEqual(mock.call_args_list[0][0][8], id(self.players[1]))

        self.assertEqual(mock.call_args_list[1][0][0], id(self.players[1]))
        self.assertEqual(mock.call_args_list[1][0][1], ith_generation)
        self.assertEqual(mock.call_args_list[1][0][2], ith_pairing)
        self.assertEqual(mock.call_args_list[1][0][3], ith_pair)
        self.assertEqual(mock.call_args_list[1][0][4], ith_round)
        self.assertEqual(mock.call_args_list[1][0][5], p2_strat)
        self.assertEqual(mock.call_args_list[1][0][6], p2_action)
        self.assertEqual(mock.call_args_list[1][0][7], p2_payoff)
        self.assertEqual(mock.call_args_list[1][0][8], id(self.players[0]))

    def test_getPlayerPayoffs_returnsProperPdPayoffs(self):
        self.assertEqual(self.subject.getRowPlayersPayoffs(0, 1), 0)
        self.assertEqual(self.subject.getRowPlayersPayoffs(1, 1), 1)
        self.assertEqual(self.subject.getRowPlayersPayoffs(0, 0), 2)

    def test_pairUpPopulation_returnsHalfLengthOfPlayers_givenEvenPlayer(self):
        self.assertEqual(
            len(self.subject.pairUpPopulation()),
            len(self.subject.population) / 2
        )

    def test_pairUpPop_returnsHalfLengthOfPlyrsMinusHalf_givenOddPlayers(self):
        players = [Player([0, 0, 0]) for i in range(7)]
        gameplay = GamePlay(players, self.pd)
        self.assertEqual(
            len(gameplay.pairUpPopulation()),
            len(gameplay.population) / 2 - 0.5
        )

    def test_pairUpWholePopulation_returnsListOfTuplesWithTwoPlayerEach(self):
        for pair in self.subject.pairUpPopulation():
            self.assertIsInstance(pair, tuple)
            self.assertIsInstance(pair[0], Player)
            self.assertIsInstance(pair[1], Player)
            self.assertEqual(len(pair), 2)

    @patch('numpy.random.shuffle')
    def test_pairUpPopulation_callsShuffleOnPlayers(self, mock):
        self.subject.pairUpPopulation()
        self.assertEqual(
            mock.call_args_list[0][0][0], self.subject.population
        )
