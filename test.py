import unittest
from game_types import *
from events import *
from game_utils import Card

class DebugDispatcher:
	def dispatch(self, updates):
		for up in updates:
			print up

class TestGameDynamics(unittest.TestCase):
	
	def test_game_starts_successfully(self):
		game = Briscola4Game(1)
		self.assertEqual(game.running, False)
		game.inject_event(SeedEvent(1))
		game.inject_event(PlayerJoinsEvent())
		game.inject_event(PlayerJoinsEvent())
		game.inject_event(PlayerJoinsEvent())
		self.assertEqual(game.running, False)
		game.inject_event(PlayerJoinsEvent())
		self.assertEqual(game.running, True)
		self.assertEqual(game.trump_suit, Card.HEARTS)
		
	def test_player_play_card(self):
		disp = DebugDispatcher()
		game = Briscola4Game(1)
		game.inject_event(SeedEvent(1),disp)
		game.inject_event(PlayerJoinsEvent(),disp)
		game.inject_event(PlayerJoinsEvent(),disp)
		game.inject_event(PlayerJoinsEvent(),disp)
		self.assertEqual(game.running, False)
		game.inject_event(PlayerJoinsEvent(),disp)
		game.inject_event(PlayCardEvent('7H'),disp)
		
	
	
if __name__ == '__main__':
    unittest.main()
