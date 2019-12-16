import unittest
from mock import patch
import numpy as np

from Python.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.simplePlayer = Player([[0, 0, 0]])
        self.titfortat_strategy = [[0, 0, 1], [1, 0, 1]]
        self.tftPlayer = Player(self.titfortat_strategy)

    def test_get_average_payoff_returns1_givenPayoffHistory1(self):
        self.simplePlayer.add_payoff_to_history(1)
        self.assertEqual(self.simplePlayer.get_average_payoff(), 1)

    def test_get_average_payoff_returns1_givenMultiplePayoffs(self):
        self.simplePlayer.add_payoff_to_history(1)
        self.simplePlayer.add_payoff_to_history(1)
        self.assertEqual(self.simplePlayer.get_average_payoff(), 1)

    def test_get_current_action_rtrnsFirstNodesAction_woStateIndexHistry(self):
        actual_action = self.simplePlayer.get_current_action(
            opponents_last_action=None)

        self.assertEqual(0, actual_action)

    def test_get_current_action_returnsCorrectActions_givenParams(self):
        actual_first_action = self.tftPlayer.get_current_action(
            opponents_last_action=None)

        self.assertEqual(0, actual_first_action)

        self.tftPlayer.update_state_index_history_with(actual_first_action)
        actual_second_action = self.tftPlayer.get_current_action(
            opponents_last_action=1)

        self.assertEqual(1, actual_second_action)

    @patch('Python.player.Player.update_state_index_history_with')
    def test_get_current_action_UpdtsStateIndexHistoryWith_noHist(self, mock):
        self.tftPlayer.get_current_action(opponents_last_action=None)

        self.assertEqual(1, mock.call_count)

    @patch('Python.player.Player.update_state_index_history_with')
    def test_get_current_action_UpdatesStateIndexHistoryWith_wHist(self, mock):
        self.tftPlayer.state_index_history.append(0)
        self.tftPlayer.get_current_action(opponents_last_action=0)

        self.assertEqual(1, mock.call_count)

    @patch('Python.player.Player.update_state_index_history_with')
    def test_get_current_action_crctlyClsUpdtStateIdxHistry_woHist(self, mock):
        self.tftPlayer.get_current_action(
            opponents_last_action=0)

        self.assertEqual(mock.call_args_list[0][0][0], 0)

    @patch('Python.player.Player.update_state_index_history_with')
    def test_get_current_action_corrctlyCallsUpdtStateIndexHistory(self, mock):
        self.tftPlayer.state_index_history.append(0)
        current_action = self.tftPlayer.get_current_action(
            opponents_last_action=0)

        self.assertEqual(mock.call_args_list[0][0][0], current_action)

    def test_get_last_state_index_returnsNone_givenEmptyStateHistory(self):
        self.assertEqual(None, self.simplePlayer.get_last_state_index())

    def test_get_last_state_index_returns1_givenStateHistoryEndingIn1(self):
        self.simplePlayer.update_state_index_history_with(0)
        self.simplePlayer.update_state_index_history_with(1)

        self.assertEqual(1, self.simplePlayer.get_last_state_index())

    def test_get_last_state_rtrn2ndState_given1asLastStateIndexHistory(self):
        self.tftPlayer.update_state_index_history_with(1)

        self.assertEqual(
            self.titfortat_strategy[1],
            self.tftPlayer.get_last_state()
        )

    def test_get_last_state_returnsNone_givenEmptyStateHistory(self):
        self.assertEqual(None, self.tftPlayer.get_last_state())

    def test_get_last_action_rtrnsDefaultActn_givenEmptyStateIndxHistory(self):
        self.assertEqual(0, self.simplePlayer.get_last_action())

    def test_get_last_action_rtrnsCorrectly_givenNonEmptyStateIndxHstry(self):
        self.tftPlayer.update_state_index_history_with(1)

        self.assertEqual(1, self.tftPlayer.get_last_action())

    def test_change_random_state_action_changesStateAction(self):
        self.simplePlayer.change_random_state_action()

        self.assertEqual(1, self.simplePlayer.strategy[0][0])

    @patch('numpy.random.randint')
    def test_change_random_state_action_changesStateAction2(self, mock):
        mock.return_value = 1
        self.tftPlayer.change_random_state_action()

        self.assertEqual(0, self.tftPlayer.strategy[0][0])

    @patch('numpy.random.choice')
    def test_rewire_random_transition_givenExtendedTFT(self, mock):
        mock.side_effect = [1, 1, 1]
        self.tftPlayer.strategy.append([1, 2, 2])
        self.tftPlayer.rewire_random_transition()

        self.assertEqual(1, self.tftPlayer.strategy[1][1])

    def test_rewire_random_transition_returnsError_givenOneState(self):
        with self.assertRaises(Exception):
            self.simplePlayer.rewire_random_transition()

    def test_add_new_state_addsOneNewStateToStrategy(self):
        old_strategy_len = len(self.simplePlayer.strategy)
        self.simplePlayer.add_new_state()

        self.assertEqual(old_strategy_len + 1, len(self.simplePlayer.strategy))

    def test_add_new_state_addsStateWith3Elements(self):
        self.simplePlayer.add_new_state()

        self.assertEqual(3, len(self.simplePlayer.strategy[-1]))

    @patch('Python.player.Player._connect_rnd_not_last_state_with_last_state')
    @patch('numpy.random.choice')
    def test_add_new_state_addsStateWith0or1AsFirstElement(self, rndChcMck, _):
        self.simplePlayer.add_new_state()
        self.assertEqual(rndChcMck.call_args_list[0][0][0], [0, 1])

    @patch('Python.player.Player._connect_rnd_not_last_state_with_last_state')
    @patch('numpy.random.choice')
    def test_add_new_state_new_st_points_to_any_other_node(self, rndChcMck, _):
        self.tftPlayer.add_new_state()
        max_node_index = len(self.tftPlayer.strategy)
        self.assertEqual(rndChcMck.call_args_list[1][0][0], max_node_index)

    def test_add_new_state_hasAtLeastOneOtherStatePointingToIt(self):
        self.tftPlayer.add_new_state()
        new_state_index = len(self.tftPlayer.strategy) - 1

        transitions = []

        for state in self.tftPlayer.strategy[:-1]:
            for transition in state[1:]:
                transitions.append(transition)
        self.assertTrue(new_state_index in transitions)

    def test_remove_state_removesOneState(self):
        old_strategy_len = len(self.tftPlayer.strategy)
        self.tftPlayer.remove_state()

        self.assertEqual(old_strategy_len - 1, len(self.tftPlayer.strategy))

    @patch('numpy.random.choice')
    def test_remove_state_choiceCalledWithCorrectParam(self, mock):
        old_strategy_length = len(self.tftPlayer.strategy)
        self.tftPlayer.remove_state()

        self.assertEqual(
            range(old_strategy_length),
            mock.call_args_list[0][0][0]
        )

    def test_remove_state_remainingTransitsPointToExistingStates(self):
        np.random.seed(99)
        self.tftPlayer.remove_state()
        available_states = range(len(self.tftPlayer.strategy))

        for state in self.tftPlayer.strategy:
            for transition in state[1:]:
                self.assertTrue(transition in available_states)

    def test_remove_state_raisesException_ifCalledOnSingleStateStrategy(self):
        with self.assertRaises(Exception):
            self.simplePlayer.remove_state()

    @ patch('Python.player.np.random.choice')
    @ patch('Python.player.Player.add_new_state')
    def test_rndmlyMutateStrat_mutatesIfFrstFindsErr(self, NwStateMck, rndMck):
        rndMck.side_effect = [
            self.simplePlayer.remove_state,
            self.simplePlayer.add_new_state
        ]
        NwStateMck.__name__ = "newState_mock"

        self.simplePlayer.randomly_mutate_strategy()

        NwStateMck.assert_called_once()
