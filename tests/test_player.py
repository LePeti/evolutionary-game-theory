import unittest

from Python.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.subject = Player([[0, 0, 0]])

    def test_getStrat_ReturnsStrat_GivenPlayerInitialisedWithStrat(self):
        self.assertEqual([[0, 0, 0]], self.subject.getStrategy())

    def test_getAveragePayoff_returns1_givenPayoffHistory1(self):
        self.subject.addPayoffToHistory(1)
        self.assertEqual(self.subject.getAveragePayoff(), 1)

    def test_getAveragePayoff_returns1_givenMultiplePayoffs(self):
        self.subject.addPayoffToHistory(1)
        self.subject.addPayoffToHistory(1)
        self.assertEqual(self.subject.getAveragePayoff(), 1)

    def test_getCurrentAction_returnsCorrectAction_givenParams(self):
        last_action_index = 0
        opponents_action = 0
        actual_action = self.subject.getCurrentAction(
            last_action_index, opponents_action)
        expected_action = 0
        self.assertEqual(expected_action, actual_action)
