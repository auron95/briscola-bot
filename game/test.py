import unittest
from games import *
from events import *
from utils import Card, Dispatcher

class DebugDispatcher(Dispatcher):
	def output(self, player, message, options):
		if message:
			print '\t'*player.index + str(message)
	
	def input(self, input_message):
		self.dispatch_game_updates(self.game.send_input(input_message))

class TestGameDynamics(unittest.TestCase):
	
	def test_game_starts_successfully(self):
		game = Briscola4Game(1)
		disp = DebugDispatcher(game)
		self.assertEqual(game.running, False)
		disp.input('1') #Seed
		disp.input('Alberto')
		disp.input('Barbara')
		disp.input('Carlo')
		disp.input('Diana')
		self.assertEqual(game.running, True)
		self.assertEqual(game.trump_suit, Card.HEARTS)
		self.assertEqual(game.players[2].hand.size(),3)
		self.assertEqual(game.deck.size(),28)
	
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
