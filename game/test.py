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
	
	def test_briscola_4(self):
		game = Briscola4Game(1)
		disp = DebugDispatcher(game)
		disp.input('1') #Seed
		disp.input('Alberto')
		disp.input('Barbara')
		disp.input('Carlo')
		disp.input('Diana')
		
		disp.input('7C')
		disp.input('6D')
		disp.input('QS')
		disp.input('3C')
		self.assertEqual(game.field.cards().size(),0)
		self.assertEqual(game.player_to_play, game.players[3])
		self.assertEqual(game.players[3].collected_points, 13)
		
		disp.input('6C') #D
		disp.input('3S') #A
		disp.input('KH') #B
		disp.input('4S') #C

		self.assertEqual(game.player_to_play, game.players[1])
		self.assertEqual(game.players[1].collected_points, 14)
		
		disp.input('7D') #B
		disp.input('QD') #C
		disp.input('2D') #D
		disp.input('2C') #A
		
		self.assertEqual(game.player_to_play, game.players[2])
		self.assertEqual(game.players[2].collected_points, 3)
		
		disp.input('5S') #C
		disp.input('AD') #D
		disp.input('3H') #A
		disp.input('JS') #B
		
		self.assertEqual(game.player_to_play, game.players[0])
		self.assertEqual(game.players[0].collected_points, 23)
		
		disp.input('KC') #A
		disp.input('AS') #B
		disp.input('4H') #C
		disp.input('5H') #D
		
		self.assertEqual(game.player_to_play, game.players[3])
		self.assertEqual(game.players[3].collected_points, 28)
		
		disp.input('4C') #D
		disp.input('JC') #A
		disp.input('4D') #B
		disp.input('2S') #C
		
		self.assertEqual(game.player_to_play, game.players[0])
		self.assertEqual(game.players[0].collected_points, 25)
		
		disp.input('QC') #A
		disp.input('2H') #B
		disp.input('7S') #C
		disp.input('KD') #D
		
		self.assertEqual(game.player_to_play, game.players[1])
		self.assertEqual(game.players[1].collected_points, 21)

		disp.input('5C') #B
		disp.input('AC') #C
		disp.input('5D') #D
		disp.input('3D') #A
		
		self.assertEqual(game.player_to_play, game.players[2])
		self.assertEqual(game.players[2].collected_points, 24)
		
		disp.input('6H') #C
		disp.input('KS') #D
		disp.input('7H') #A
		disp.input('QH') #B
		
		self.assertEqual(game.player_to_play, game.players[1])
		self.assertEqual(game.players[1].collected_points, 28)

		disp.input('AH') #B
		disp.input('JD') #C
		disp.input('6S') #D
		disp.input('JH') #A

		self.assertEqual(game.player_to_play, game.players[1])
		self.assertEqual(game.players[1].collected_points, 43)

		self.assertEqual(sum(map(lambda p: p.collected_points, game.players)), 120)
		self.assertEqual(game.players[0].collected_cards.value(), game.players[0].collected_points)

		
	
	
if __name__ == '__main__':
    unittest.main()
