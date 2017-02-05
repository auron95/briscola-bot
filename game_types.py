from game_utils import *
from models import Game
from events import *

class Briscola4Game(Game):
	Card = Card
	
	NUMBER_OF_PLAYERS = 4
	TYPE_OF_AUCTION = None
	INITIAL_HAND_SIZE = 3
	DRAW_AFTER_TRICK = True
	MUST_RESPOND_TO_SUIT = False
	HEARTS_MUST_BE_BROKEN = False

	def trigger_automatic(self, dispatcher):
		if not self.running and len(self.players) == self.NUMBER_OF_PLAYERS:
			self.inject_event(InitializeEvent(), dispatcher)
		elif self.running and not self.trump_suit:
			self.inject_event(SetTrumpEvent(), dispatcher)
		elif len(self.field.cards()) == self.NUMBER_OF_PLAYERS:
			self.inject_event(TakeTrickEvent(), dispatcher)
		
	__mapper_args__ = {
		'polymorphic_identity':'briscola4game'
    }
