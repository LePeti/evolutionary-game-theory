import unittest
from mock import patch

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

    def test_getCurrentAction_returnsFirstNodesAction_woStateIndexHistry(self):
        actual_action = self.simplePlayer.getCurrentAction(
            opponents_last_action=None)

        self.assertEqual(0, actual_action)

    def test_getCurrentAction_returnsCorrectActions_givenParams(self):
        actual_first_action = self.tftPlayer.getCurrentAction(
            opponents_last_action=None)

        self.assertEqual(0, actual_first_action)

        self.tftPlayer.updateStateIndexHistoryWith(actual_first_action)
        actual_second_action = self.tftPlayer.getCurrentAction(
            opponents_last_action=1)

        self.assertEqual(1, actual_second_action)

    @patch('Python.player.Player.updateStateIndexHistoryWith')
    def test_getCurrentAction_UpdatesStateIndexHistoryWith_noHist(self, mock):
        self.tftPlayer.getCurrentAction(opponents_last_action=None)

        self.assertEqual(1, mock.call_count)

    @patch('Python.player.Player.updateStateIndexHistoryWith')
    def test_getCurrentAction_UpdatesStateIndexHistoryWith_wHist(self, mock):
        self.tftPlayer.state_index_history.append(0)
        self.tftPlayer.getCurrentAction(opponents_last_action=0)

        self.assertEqual(1, mock.call_count)

    @patch('Python.player.Player.updateStateIndexHistoryWith')
    def test_getCurrentAction_crrctlyCllsUpdtStateIdxHistry_woHist(self, mock):
        self.tftPlayer.getCurrentAction(
            opponents_last_action=0)

        self.assertEqual(mock.call_args_list[0][0][0], 0)

    @patch('Python.player.Player.updateStateIndexHistoryWith')
    def test_getCurrentAction_correctlyCallsUpdtStateIndexHistory(self, mock):
        self.tftPlayer.state_index_history.append(0)
        current_action = self.tftPlayer.getCurrentAction(
            opponents_last_action=0)

        self.assertEqual(mock.call_args_list[0][0][0], current_action)

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

    def test_changeRandomStateAction_changesStateAction(self):
        self.simplePlayer.changeRandomStateAction()

        self.assertEqual(1, self.simplePlayer.strategy[0][0])

    @patch('numpy.random.randint')
    def test_changeRandomStateAction_changesStateAction2(self, mock):
        mock.return_value = 1
        self.tftPlayer.changeRandomStateAction()

        self.assertEqual(0, self.tftPlayer.strategy[0][0])

    @patch('numpy.random.choice')
    def test_rewireRandomTransition_givenExtendedTFT(self, mock):
        mock.side_effect = [1, 1, 1]
        self.tftPlayer.strategy.append([1, 2, 2])
        self.tftPlayer.rewireRandomTransition()

        self.assertEqual(1, self.tftPlayer.strategy[1][1])

    def test_rewireRandomTransition_returnsError_givenOneState(self):
        with self.assertRaises(Exception):
            self.simplePlayer.rewireRandomTransition()
