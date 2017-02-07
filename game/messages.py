# coding=utf8

class EventMessage:
	BROADCASTED_MESSAGE = None
	PERSONAL_MESSAGE = None
	
	def __init__(self, player=None, **kwargs):
		self.player = player #Player who receives the message
		self.kwargs = kwargs
		
	def ita(self,player=None):
		assert (player or 'PERSONAL_MESSAGE' in self.ita_string)
		if player != self.player:
			if 'BROADCASTED_MESSAGE' in self.ita_string:
				return self.ita_string['BROADCASTED_MESSAGE'].format(**self.kwargs)
		else:
			return self.ita_string['PERSONAL_MESSAGE'].format(**self.kwargs)
		
	def options(self, player):
		if 'options' in self.kwargs and player == self.player: 
			return self.kwargs['options']
			
		
class PlayedCardMessage(EventMessage):
	ita_string = {
		'BROADCASTED_MESSAGE': '{name} ha giocato {card}', 
		'PERSONAL_MESSAGE': 'Hai giocato {card}'
	}

class TrickTakenMessage(EventMessage):
	ita_string = {
		'BROADCASTED_MESSAGE': '{name} ha preso {cards}!', 
		'PERSONAL_MESSAGE': 'Hai preso {cards}'
	}
	
class StartedGameMessage(EventMessage):
	ita_string = {
		'BROADCASTED_MESSAGE': 'La partita è iniziata! Inizierà {name}', 
	}
	
class PlayerJoinedMessage(EventMessage):
	ita_string = {
		'BROADCASTED_MESSAGE': '{name} si è unito!', 
		'PERSONAL_MESSAGE': 'Ti sei unito.'
	}

class IllegalMoveMessage(EventMessage):
	ita_string = {
		'PERSONAL_MESSAGE': 'Mossa non valida'
	}
	
class CardDrawnMessage(EventMessage):
	ita_string = {
		'PERSONAL_MESSAGE': 'Hai pescato {cards}'
	}
	
class TrumpRevealedMessage(EventMessage):
	ita_string = {
		'BROADCASTED_MESSAGE': "In fondo al mazzo c'è {card}!"
	}
	
