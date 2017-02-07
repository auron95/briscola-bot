from utils import *
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
	
	def send_input(self, value):
		if not hasattr(self,'random'):
			return self._inject_event(SeedEvent(int(value)))
		if len(self.players) < self.NUMBER_OF_PLAYERS:
			return self._inject_event(PlayerJoinsEvent(value))
		
		return self._inject_event(PlayCardEvent(value))

	def trigger_automatic(self):
		if not self.running:
			if len(self.players) == self.NUMBER_OF_PLAYERS:
				return self._inject_event(InitializeEvent())
		else:
			if not self.trump_suit:
				return self._inject_event(SetTrumpEvent())
				
			if self.field.cards().size() == self.NUMBER_OF_PLAYERS:
				return self._inject_event(TakeTrickEvent())
		
			if self.player_to_play.hand.size() < 3 and self.deck.size > 0:
				return self._inject_event(DrawCardEvent(3-self.player_to_play.hand.size()))
				
		return []
		
	__mapper_args__ = {
		'polymorphic_identity':'briscola4game'
    }
