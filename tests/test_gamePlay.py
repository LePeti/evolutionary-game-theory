import unittest
from game_play import *
from game import *
from player import *
import numpy as np


class TestGamePlay(unittest.TestCase):

    def setUp(self):
        self.player1 = Player([0])
        self.player2 = Player([1])
        self.game = Game(np.array([[2, 0], [4, 1]]))
        self.subject = GamePlay(self.player1, self.player2, self.game)

    def test_getPlayer_ReturnsPlayerInstance_givenPlayer1Or2(self):
        self.assertIsInstance(self.subject.players[0], Player)
        self.assertIsInstance(self.subject.players[1], Player)

    def test_game_ReturnsGameInstance(self):
        self.assertIsInstance(self.subject.game, Game)

    def test_getGame_ReturnsSpecGameInstance_givenSpecGame(self):
        self.assertEqual(self.subject.game, self.game)
