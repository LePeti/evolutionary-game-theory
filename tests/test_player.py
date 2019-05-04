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
        actual_action = self.simplePlayer.getCurrentAction(
            opponents_last_action=None)

        self.assertEqual(0, actual_action)

    def test_getCurrentAction_returnsCorrectAction_givenParams(self):
        actual_action = self.simplePlayer.getCurrentAction(
            opponents_last_action=0)

        self.assertEqual(0, actual_action)

    def test_getCurrentAction_returnsCorrectActions_givenParams(self):
        actual_first_action = self.tftPlayer.getCurrentAction(
            opponents_last_action=None)

        self.assertEqual(0, actual_first_action)

        self.tftPlayer.updateStateIndexHistoryWith(actual_first_action)
        actual_second_action = self.tftPlayer.getCurrentAction(
            opponents_last_action=1)

        self.assertEqual(1, actual_second_action)

    def test_getLastStateIndex_returnsNone_givenEmptyStateHistory(self):
        self.assertEqual(None, self.simplePlayer.getLastStateIndex())

    def test_getLastStateIndex_returns1_givenStateHistoryEndingIn1(self):
        self.simplePlayer.updateStateIndexHistoryWith(0)
        self.simplePlayer.updateStateIndexHistoryWith(1)

        self.assertEqual(1, self.simplePlayer.getLastStateIndex())

    def test_getLastState_returns2ndState_given1asLastStateIndexHistory(self):
        self.tftPlayer.updateStateIndexHistoryWith(1)

        self.assertEqual(
            self.titfortat_strategy[1],
            self.tftPlayer.getLastState()
        )

    def test_getLastState_returnsNone_givenEmptyStateHistory(self):
        self.assertEqual(None, self.tftPlayer.getLastState())

    def test_getLastAction_returnsDefaultActn_givenEmptyStateIndxHistory(self):
        self.assertEqual(0, self.simplePlayer.getLastAction())

    def test_getLastAction_returnsCorrectly_givenNonEmptyStateIndxHstry(self):
        self.tftPlayer.updateStateIndexHistoryWith(1)

        self.assertEqual(1, self.tftPlayer.getLastAction())
