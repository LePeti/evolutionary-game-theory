import unittest
from player import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.subject = Player(0)

    def test_getStrategy_ReturnsStrat_GivenPlayerInitialisedWithStrat(self):
        self.assertEqual(0, self.subject.getStrategy())
