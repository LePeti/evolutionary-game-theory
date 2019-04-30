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
        self.players = [Player([0, 0, 0]), Player(
            [1, 0, 0]), Player([1, 0, 0]), Player([1, 0, 0])]
        self.subject = GamePlay(self.players, self.pd)

    @patch('Python.player.Player.addPayoffToHistory')
    def test_playRound_callsaddPayoffToHistoryTwice(self, mock):
        self.subject.playRound(self.players[0:2])
        self.assertEqual(mock.call_count, 2)

    @patch('Python.game_play.GamePlay.addRoundToHistory')
    def test_playRound_callsaddRoundToHistoryWithCorrectParams(self, mock):
        selectedPlayers = self.players[0:2]
        self.subject.playRound(selectedPlayers)
        actions = tuple(player.getStrategy() for player in selectedPlayers)
        round_payoffs = self.subject.getPlayerPayoffs(*actions)
        self.assertEqual(mock.call_args_list[0][0][0], actions)
        self.assertEqual(mock.call_args_list[0][0][1], round_payoffs)

    def test_getPlayerPayoffs_returnsProperPdPayoffs(self):
        payoffs04 = self.subject.getPlayerPayoffs(0, 1)
        self.assertEqual(payoffs04, (0, 4))

        payoffs11 = self.subject.getPlayerPayoffs(1, 1)
        self.assertEqual(payoffs11, (1, 1))

        payoffs22 = self.subject.getPlayerPayoffs(0, 0)
        self.assertEqual(payoffs22, (2, 2))

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
