	
class Player
	def __init__ (self, chat_id, index, name):
		self.chat_id = chat_id
		self.index = index
		self.name = name
		self.last_message = None

class GameUpdateMessage:
	def __init__(self, player_id, message, options):
		self.player_id = player_id
		self.message = message
		self.options = options
		
	def __repr__(self):
		return "P" + str(self.player_id) + " << " +  self.message + "\n" + str(self.options)
		

