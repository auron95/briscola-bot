import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

Base = declarative_base()

class KnowsChild(object):
    # Make a place to store the class name of the child
    # (copied almost entirely from http://blog.headspin.com/?p=474)
    subclass = Column(String)
  
    def as_child(self):
        return getattr(self, self.subclass.lower())

    def fill_subclass(self):
        self.subclass = self.__class__.__name__

    def save(self, *args, **kwargs):
        self.fill_subclass()
        super(KnowsChild, self).save(*args, **kwargs)

class Event(KnowsChild, Base):
	__tablename__ = 'events'

	id = Column(Integer, primary_key=True)
	value = Column(String)
	
	
	def __init__(self, value=None):
		self.value = None
		update_messages = []
	
	def resolve(self, game):
		raise NotImplementedError("Event has no resolve method") 
		
	def trigger_after(self, game):
		pass
		
	def send_update(game, update):
		self.update_messages.append(update)
		update.player.last_message = update

class Game(Base):
	__tablename__ = 'games'
	NUMBER_OF_PLAYERS = None
	name = Column(String, primary_key=True)
	
	def __init__ (self, id):
		self.id = id
		self.players = []
		self.deck = []
		self.player_to_play = None
		self.events = []
	
	def inject_event(self, event, dispatcher = None):
		event.resolve(self)
		if dispatcher:
			dispatcher.dispatch(event.update_messages)
		game.trigger_automatic(dispatcher)
		return 
		
	def _update(self):
		while len(self.events) > 0:
			event = self.events.pop(0)
			event.resolve(self)
			
		
	def trigger_automatic(self, dispatcher):
		raise NotImplementedError("Game has no trigger_automatic method") 
		
		
		
