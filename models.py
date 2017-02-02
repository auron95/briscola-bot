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
	dvalue = Column(String)
	player_id = Column(Integer)
	
	update_messages = []
	
	def __init__(self, value=None, player_id=None):
		self.player_id = player_id
		self.value = None
	
	def trigger(self, game):
		raise NotImplementedError("Trigger is not implemented") 

class Game(Base):
	__tablename__ = 'games'
	name = Column(String, primary_key=True)
	
	def __init__ (self, id):
		self.id = id
		self.players = []
