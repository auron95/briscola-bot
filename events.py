from game_utils import GameUpdateMessage, Player
from models import Event
import random
from errors import *
from game_utils import Deck

class SeedEvent(Event):

	def resolve(self, game):
		random.seed(int(self.value))
		game.random = random

class PlayCardEvent(Event):
	
	def resolve(self, game):
		player = game.player_to_play
		if player is None:
			raise UnexpectedEvent('PlayCardEvent received, but no player was expected to play.')
		
		card = game.Card(self.value)

		player.play(card)
		
		self.send_update(game,GameUpdateMessage(player, 'Hai giocato '+str(card)+'!', player.hand))
		for pl in game.players:
			if pl != player:
				self.send_update(game,GameUpdateMessage(pl, pl.name + ' ha giocato ' + str(card)+'!', player.hand))
				
		game.player_to_play = player.next()

	def __repr__(self):
		return 'A player plays ' + str(self.value)

class TakeTrickEvent(Event):
	def resolve(self, game):
		player = game.field.get_taking_play()[0]
		player.current_points += game.field.points_on_the_field()
		player.collected_card.append(game.fields.cards())
		assert(sum(map(lambda card: card.value(), player.collected_cards))==player.current_points)
		
		self.send_update(game,GameUpdateMessage(player, 'Hai preso tu!', player.hand))
		for pl in game.players:
			if pl != player:
				self.send_update(game, GameUpdateMessage(pl, player.name + ' ha preso!', pl.hand))
			if game.DRAW_AFTER_TRICK:
				drawn = player.draw(game.deck)
				pl.send_update(pl, 'Hai pescato ' + str(drawn) + '!')
		game.player_to_play = player
		
	def __repr__(self):
		return "End of the trick."
		
class InitializeEvent(Event):
	def resolve(self, game):
		game.deck = Deck(game.Card)
		assert(game.deck.size() == 40)
		game.deck.shuffle(game.random)
		game.running = True
		for player in game.players:
			drawn = player.draw(game.deck, game.INITIAL_HAND_SIZE)
			self.send_update(game, GameUpdateMessage(player, 'Hai pescato ' + " ".join(str(card) for card in drawn), player.hand))
		game.player_to_play=game.players[0]
			
class PlayerJoinsEvent(Event):
	def resolve(self,game):
		game.players.append(Player(game,len(game.players)))

class SetTrumpEvent(Event):
	def resolve(self, game):
		last_card = game.deck.cards[-1]
		game.trump_suit = last_card.suit
		for player in game.players:
			self.send_update(game, GameUpdateMessage(player, "C'e` un " + str(last_card) + " in fondo al mazzo!", player.hand))
	

	

	
	
