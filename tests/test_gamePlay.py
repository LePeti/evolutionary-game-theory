import unittest
import numpy as np
from mock import patch

from Python.game_play import *
from Python.game import *
from Python.player import *


class TestGamePlay(unittest.TestCase):

    def setUp(self):
        self.pd = Game(np.array([[2, 0],
                                 [4, 1]])
                       )
        self.players = [Player([[0, 0, 0]]), Player(
            [[1, 0, 0]]), Player([[1, 0, 0]]), Player([[1, 0, 0]])]
        self.subject = GamePlay(self.players, self.pd)

    @patch('Python.player.Player.addPayoffToHistory')
    def test_playRound_callsaddPayoffToHistoryTwice(self, mock):
        self.subject.playRound(self.players[0], self.players[1])
        self.assertEqual(mock.call_count, 2)

    @patch('Python.game_play.GamePlay.addRoundToGameHistory')
    def test_playRound_callsaddRoundToGameHistoryWithCorrectParams(self, mock):
        selectedPlayers = self.players[0:2]
        self.subject.playRound(*selectedPlayers)

        p1_action = selectedPlayers[0].strategy[0][0]
        p2_action = selectedPlayers[1].strategy[0][0]
        p1_payoff = self.subject.getRowPlayersPayoffs(p1_action, p2_action)
        p2_payoff = self.subject.getRowPlayersPayoffs(p2_action, p1_action)

        self.assertEqual(mock.call_args_list[0][0][0], p1_action)
        self.assertEqual(mock.call_args_list[0][0][1], p2_action)
        self.assertEqual(mock.call_args_list[0][0][2], p1_payoff)
        self.assertEqual(mock.call_args_list[0][0][3], p2_payoff)

    def test_getPlayerPayoffs_returnsProperPdPayoffs(self):
        expected_payoff = self.subject.getRowPlayersPayoffs(0, 1)
        self.assertEqual(expected_payoff, 0)

        expected_payoff = self.subject.getRowPlayersPayoffs(1, 1)
        self.assertEqual(expected_payoff, 1)

        expected_payoff = self.subject.getRowPlayersPayoffs(0, 0)
        self.assertEqual(expected_payoff, 2)

    def test_pairUpPopulation_returnsHalfLengthOfPlayers_givenEvenPlayer(self):
        self.assertEqual(
            len(self.subject.pairUpPopulation()),
            len(self.subject.population) / 2
        )

    def test_pairUpPop_returnsHalfLengthOfPlyrsMinusHalf_givenOddPlayers(self):
        players = [Player(np.random.choice([0, 1])) for i in range(7)]
        alt_subject = GamePlay(players, self.pd)
        self.assertEqual(
            len(alt_subject.pairUpPopulation()),
            len(alt_subject.population) / 2 - 0.5
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
