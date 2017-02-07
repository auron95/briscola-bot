from utils import Player
from messages import *
from models import Event
import random
from errors import *
from utils import Deck

class SeedEvent(Event):

	def resolve(self, game):
		random.seed(int(self.value))
		game.random = random

	__mapper_args__ = {
		'polymorphic_identity':'seed_event'
	}

class PlayCardEvent(Event):
	
	__mapper_args__ = {
		'polymorphic_identity':'play_card_event'
	}

	def resolve(self, game):
		player = game.player_to_play
		if player is None:
			raise UnexpectedEvent('PlayCardEvent received, but no player was expected to play.')
		
		card = game.Card(self.value)

		player.play(card)
		
		game.player_to_play = player.next()
		return PlayedCardMessage(player, name = player.name, options = player.hand, card=card)

	def __repr__(self):
		return 'A player plays ' + str(self.value)

class TakeTrickEvent(Event):

	__mapper_args__ = {
		'polymorphic_identity':'take_trick_event'
	}

	def resolve(self, game):
		player = game.field.get_taking_play(game.trump_suit)[0]
		player.collected_points += game.field.points_on_the_field()
		player.collected_cards.cards += game.field.cards().cards
		game.field.clear()
		game.player_to_play=player
		return TrickTakenMessage(player, name=player.name, cards = game.field.cards())
		
	def __repr__(self):
		return "End of the trick."

class DrawCardEvent(Event):

	__mapper_args__ = {
		'polymorphic_identity':'draw_card_event'
	}

	def resolve(self,game):
		player = game.player_to_play 
		drawn = player.draw(game.deck, int(self.value))
		game.player_to_play = player.next()
		return CardDrawnMessage(player, cards = drawn)
		
class InitializeEvent(Event):

	__mapper_args__ = {
		'polymorphic_identity':'initialize_game_event'
	}

	def resolve(self, game):
		game.deck = Deck(game.Card)
		assert(game.deck.size() == 40)
		game.deck.shuffle(game.random)
		game.running = True
		game.player_to_play=game.players[0]
		return StartedGameMessage(name = game.player_to_play.name)
			
class PlayerJoinsEvent(Event):
	
	__mapper_args__ = {
		'polymorphic_identity':'player_joins_event'
	}

	def resolve(self,game):
		game.players.append(Player(game,len(game.players),self.value))
		return PlayerJoinedMessage(game.players[-1], name=game.players[-1].name)

class SetTrumpEvent(Event):

	__mapper_args__ = {
		'polymorphic_identity':'set_trump_event'
	}

	def resolve(self, game):
		last_card = game.deck.cards[-1]
		game.trump_suit = last_card.suit
		return TrumpRevealedMessage(card=last_card)
	

	
	
