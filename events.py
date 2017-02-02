from game import GameUpdateMessage, Player
from models import Event
import random
from errors import *

class SeedEvent(Event):

	def trigger(self, game)
		random.seed(int(self.value))
		game.generate_random = random.random


	

	
	
