from game import GameUpdateMessage, Player, Card
from models import Event
import random
from errors import *

class SeedEvent(Event):

	def resolve(self, game):
		random.seed(int(self.value))
		game.random = random

class PlayCardEvent(Event):
	
	def resolve(self, game):
		player = game.player_turn
		if player is None:
			raise UnexpectedEvent('PlayCardEvent received, but no player was expected to play.')
		
		card = Card(self.value)

		player.play(card)
		
		self.send_update(GameUpdateMessage(player, 'Hai giocato '+str(card)+'!',player.hand))
		for pl in game.players:
			if pl != player:
				self.send_update(GameUpdateMessage(pl, pl.name + ' ha giocato ' + str(card)+'!')) 
		
	


	#def trigger_after(self, game):
	#	assert (len(game.table) <= game.NUMBER_OF_PLAYERS)
	#	if len(game.table) == game.NUMBER_OF_PLAYERS:
	#		game.inject_event(TakeTrickEvent())
	
	def __repr__(self):
		return 'A player plays ' + str(self.value)

		
	


	

	
	
