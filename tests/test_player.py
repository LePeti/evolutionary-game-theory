import unittest
from player import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.subject = Player(0)

    def test_getStrategy_ReturnsStrat_GivenPlayerInitialisedWithStrat(self):
        self.assertEqual(0, self.subject.getStrategy())

    def test_getAveragePayoff_returns1_givenPayoffHistory1(self):
        self.subject.addPayoff(1)
        self.assertEqual(self.subject.getAveragePayoff(), 1)
