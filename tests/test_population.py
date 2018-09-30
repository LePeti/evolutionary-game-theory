import unittest
import numpy as np
from mock import patch

from population import *
from player import *


class TestGamePlay(unittest.TestCase):
    def setUp(self):
        self.subject = Population(
            [Player(np.random.choice([0, 1])) for i in range(4)]
        )

    def test_pairTwoRndPlayers_selectsTwoThings(self):
        self.assertEqual(len(self.subject.pairTwoRndPlayers()), 2)

    def test_pairTwoRndPlayers_selectsPlayerInstances(self):
        self.assertIsInstance(self.subject.pairTwoRndPlayers()[0], Player)
        self.assertIsInstance(self.subject.pairTwoRndPlayers()[1], Player)

    @patch('numpy.random.choice')
    def test_pairTwoRndPlayers_selectsRandomlyFromSubjectStrategies(self, mock):
        self.subject.pairTwoRndPlayers()
        self.assertEqual(
            mock.call_args_list[0][0][0], self.subject.players
        )

    def test_pairUpPopulation_returnsHalfLengthOfPlayers_givenEvenPlayers(self):
        self.assertEqual(
            len(self.subject.pairUpPopulation()),
            len(self.subject.players) / 2
        )

    def test_pairUpPop_returnsHalfLengthOfPlyrsMinusHalf_givenEvenPlayers(self):
        alt_subject = Population(
            [Player(np.random.choice([0, 1])) for i in range(7)])
        self.assertEqual(
            len(alt_subject.pairUpPopulation()),
            len(alt_subject.players) / 2 - 0.5
        )

    def test_pairUpWholePopulation_returnsListOfTuples(self):
        for pair in self.subject.pairUpPopulation():
            self.assertIsInstance(pair, tuple)
