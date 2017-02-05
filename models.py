import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

from game_utils import Field
from errors import IllegalMove
Base = declarative_base()

class Event(Base):
	__tablename__ = 'events'

	id = Column(Integer, primary_key=True)
	value = Column(String)
	
	type = Column(String(30))
	__mapper_args__ = {
		'polymorphic_on':type,
		'polymorphic_identity':'employee'
	}

	def __init__(self, value=None):
		self.value = value
		self.update_messages = []
	
	def resolve(self, game):
		raise NotImplementedError("Event has no resolve method") 
		
	def trigger_after(self, game):
		pass
		
	def send_update(self, game, update):
		self.update_messages.append(update)
		update.player.last_message = update


class Game(Base):
	__tablename__ = 'games'
	NUMBER_OF_PLAYERS = None
	TYPE_OF_AUCTION = None
	INITIAL_HAND_SIZE = None
	DRAW_AFTER_TRICK = False
	MUST_RESPOND_TO_SUIT = False
	HEARTS_MUST_BE_BROKEN = False
	
	
	Card = None
	name = Column(String, primary_key=True)
	
	type = Column(String(30))
	
	__mapper_args__ = {
		'polymorphic_on':type,
		'polymorphic_identity':'game'
	}
	
	
	def __init__ (self, id):
		self.id = id
		self.players = []
		self.deck = []
		self.player_to_play = None
		self.events = []
		self.field = Field()
		self.deck = []
		self.running = False
		self.trump_suit = None
	
	def inject_event(self, event, dispatcher = None):
		try:
			event.resolve(self)
			if dispatcher:
				dispatcher.dispatch(event.update_messages)
			self.trigger_automatic(dispatcher)
		except IllegalMove:
			self.trigger_automatic(dispatcher)
		return 
		
	def _update(self):
		while len(self.events) > 0:
			event = self.events.pop(0)
			event.resolve(self)
			
		
	def trigger_automatic(self, dispatcher):
		raise NotImplementedError("Game has no trigger_automatic method") 
		
		
		
