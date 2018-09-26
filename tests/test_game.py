import unittest
from game import *
import numpy as np


class TestGame(unittest.TestCase):

    def setUp(self):
        self.pd_payoff = np.array([[2, 0], [4, 1]])
        self.subject = Game(self.pd_payoff)

    def test_getPayoff_ReturnsSimplePO_GivenGameInitialisedWithSimplePO(self):
        simple_payoff = np.array([0])
        game_w_simple_payoff = Game(simple_payoff)
        np.testing.assert_array_equal(
            simple_payoff,
            game_w_simple_payoff.getPayoff()
        )

    def test_getPayoffHistory_ReturnsPDPO_GivenGameInitialisedWithPDPO(self):
        np.testing.assert_array_equal(
            self.pd_payoff,
            self.subject.getPayoff()
        )
