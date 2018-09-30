import unittest
import numpy as np
from mock import patch

from population import *
from player import *


class TestGamePlay(unittest.TestCase):
    def setUp(self):
        self.subject = Population(
            [Player(np.random.choice([0, 1])) for i in range(3)]
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
