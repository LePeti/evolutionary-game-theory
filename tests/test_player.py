import unittest
from mock import patch
import numpy as np

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

    def test_addNewState_addsOneNewStateToStrategy(self):
        old_strategy_len = len(self.simplePlayer.strategy)
        self.simplePlayer.addNewState()

        self.assertEqual(old_strategy_len + 1, len(self.simplePlayer.strategy))

    def test_addNewState_addsStateWith3Elements(self):
        self.simplePlayer.addNewState()

        self.assertEqual(3, len(self.simplePlayer.strategy[-1]))

    @patch('Python.player.Player._connectRndNotLastStateWithLastState')
    @patch('numpy.random.choice')
    def test_addNewState_addsStateWith0or1AsFirstElement(self, rndChcMck, _):
        self.simplePlayer.addNewState()

        self.assertEqual(rndChcMck.call_args_list[0][0][0], [0, 1])

    @patch('Python.player.Player._connectRndNotLastStateWithLastState')
    @patch('numpy.random.choice')
    def test_addNewState_assigns0or1TransitionsRandomly(self, rndChcMck, _):
        self.simplePlayer.addNewState()

        self.assertEqual(rndChcMck.call_args_list[1][0][0], [0, 1])

    def test_addNewState_hasAtLeastOneOtherStatePointingToIt(self):
        self.tftPlayer.addNewState()
        new_state_index = len(self.tftPlayer.strategy) - 1

        transitions = []

        for state in self.tftPlayer.strategy[:-1]:
            for transition in state[1:]:
                transitions.append(transition)
        self.assertTrue(new_state_index in transitions)

    def test_removeState_removesOneState(self):
        old_strategy_len = len(self.tftPlayer.strategy)
        self.tftPlayer.removeState()

        self.assertEqual(old_strategy_len - 1, len(self.tftPlayer.strategy))

    @patch('numpy.random.choice')
    def test_removeState_choiceCalledWithCorrectParam(self, mock):
        old_strategy_length = len(self.tftPlayer.strategy)
        self.tftPlayer.removeState()

        self.assertEqual(
            range(old_strategy_length),
            mock.call_args_list[0][0][0]
        )

    def test_rmvState_remainingTransitsPointToExistingStates(self):
        np.random.seed(99)
        self.tftPlayer.removeState()
        available_states = range(len(self.tftPlayer.strategy))

        for state in self.tftPlayer.strategy:
            for transition in state[1:]:
                self.assertTrue(transition in available_states)

    def test_removeState_raisesException_ifCalledOnSingleStateStrategy(self):
        with self.assertRaises(Exception):
            self.simplePlayer.removeState()

    @ patch('Python.player.np.random.choice')
    @ patch('Python.player.Player.addNewState')
    def test_rndmlyMutateStrat_mutatesIfFrstFindsErr(self, NwStateMck, rndMck):
        rndMck.side_effect = [
            self.simplePlayer.removeState,
            self.simplePlayer.addNewState
        ]
        NwStateMck.__name__ = "newState_mock"

        self.simplePlayer.randomlyMutateStrategy()

        NwStateMck.assert_called_once()
