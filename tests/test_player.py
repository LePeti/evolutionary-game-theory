import unittest

from Python.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.subject = Player(0)

    def test_getAction_ReturnsStrat_GivenPlayerInitialisedWithStrat(self):
        self.assertEqual(0, self.subject.getStrategy())

    def test_getAveragePayoff_returns1_givenPayoffHistory1(self):
        self.subject.addPayoffToHistory(1)
        self.assertEqual(self.subject.getAveragePayoff(), 1)

    def test_getAveragePayoff_returns1_givenMultiplePayoffs(self):
        self.subject.addPayoffToHistory(1)
        self.subject.addPayoffToHistory(1)
        self.assertEqual(self.subject.getAveragePayoff(), 1)
