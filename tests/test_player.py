import unittest

from Python.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.simplePlayer = Player([[0, 0, 0]])
        self.titfortat_strategy = [[0, 0, 1], [1, 0, 1]]
        self.tftPlayer = Player(self.titfortat_strategy)

    def test_getAveragePayoff_returns1_givenPayoffHistory1(self):
        self.simplePlayer.addPayoffToHistory(1)
        self.assertEqual(self.simplePlayer.getAveragePayoff(), 1)

    def test_getAveragePayoff_returns1_givenMultiplePayoffs(self):
        self.simplePlayer.addPayoffToHistory(1)
        self.simplePlayer.addPayoffToHistory(1)
        self.assertEqual(self.simplePlayer.getAveragePayoff(), 1)

    def test_getCurrentAction_returnsFirstNodesAction_notGivenParams(self):
        opponents_last_action = None

        actual_action = self.simplePlayer.getCurrentAction(
            opponents_last_action)
        expected_action = 0
        self.assertEqual(expected_action, actual_action)

    def test_getCurrentAction_returnsCorrectAction_givenParams(self):
        last_action_index = 0
        opponents_last_action = 0

        actual_action = self.simplePlayer.getCurrentAction(
            opponents_last_action)
        expected_action = 0
        self.assertEqual(expected_action, actual_action)

    def test_getCurrentAction_returnsCorrectActions_givenParams(self):
        actual_first_action = self.tftPlayer.getCurrentAction(
            opponents_last_action=None)
        expected_first_action = 0

        self.assertEqual(expected_first_action, actual_first_action)

        self.tftPlayer.updateStateIndexHistoryWith(expected_first_action)
        actual_second_action = self.tftPlayer.getCurrentAction(
            opponents_last_action=1)
        expected_second_action = 1

        self.assertEqual(expected_second_action, actual_second_action)

    def test_getLastStateIndex_returnsNone_givenEmptyStateHistory(self):
        self.assertEqual(None, self.simplePlayer.getLastStateIndex())

    def test_getLastStateIndex_returns1_givenStateHistoryEndingIn1(self):
        self.simplePlayer.updateStateIndexHistoryWith(0)
        self.simplePlayer.updateStateIndexHistoryWith(1)

        self.assertEqual(1, self.simplePlayer.getLastStateIndex())

    def test_getLastState_returns2ndState_given1asLastStateIndexHistory(self):
        self.tftPlayer.updateStateIndexHistoryWith(1)

        expected_state = self.titfortat_strategy[1]
        actual_state = self.tftPlayer.getLastState()

        self.assertEqual(expected_state, actual_state)

    def test_getLastState_returnsNone_givenEmptyStateHistory(self):
        expected_state = None
        actual_state = self.tftPlayer.getLastState()

        self.assertEqual(expected_state, actual_state)
