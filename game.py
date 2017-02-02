from errors import *

class Player:
	def __init__ (self, chat_id, index, name, game):
		self.chat_id = chat_id
		self.index = index
		self.name = name
		self.last_message = None
		self.game = game
	
	def __repr__(self):
		return str(self.name) + "(Giocatore " + str(self.index) + ")"
		
	def draw(self, deck):
		self.hand.append(deck.draw())
	
	def card_index(self,card):
		# Check if player has a card, and return that if found
		matches = [i for i, c in enumerate(self.hand) if str(c) == str(card)]
		assert(len(matches)<=1)
		if len(matches) == 0:
			return None
		else:
			return matches[0]
	
	def play(self,card):
		index = self.card_index(card)
		if index==None:
			raise CardNotFound(self.player + " tried to play " + self.card + " but that was not in his hand.")
		else:
			self.game.table.append((self, self.hand.pop(index)))
			assert(self.card_index(card)==None)
	
class Field:
	def __init__(self):
		self.plays = []

	def get_taking_play(self):
		return max(self.plays, lambda p: p[1].taking_power())
 
	
class Card:
	NUMBERS = ["2","3","4","5","6","7","J","Q","K","A"];
	HEARTS = '\xE2\x99\xA5\xEF\xB8\x8F'
	DIAMONDS = '\xE2\x99\xA6\xEF\xB8\x8F'
	CLUBS = '\xE2\x99\xA3\xEF\xB8\x8F'
	SPADES = '\xE2\x99\xA0\xEF\xB8\x8F'
	SUITS = [HEARTS, DIAMONDS, CLUBS, SPADES]
	
	ASCII_SUITS = {
		'H':HEARTS,
		'D':DIAMONDS,
		'S':SPADES,
		'C':CLUBS
	}
	
	
	VALUES = {
		"A": 11,
		"K": 4,
		"Q": 3,
		"J": 2
	}
	
	def __init__ (self, name):		
		self.suit = name[1:]
		if self.suit in self.ASCII_SUITS:
			self.suit = self.ASCII_SUITS[self.suit]
		
		if self.suit not in self.SUITS:
			raise NotAValidCard(self.suit + " is not a valid suit.")
		
		self.number = name[:1]
		if self.number not in self.NUMBERS:
			raise NotAValidCard(self.number + " is not a valid number.")

	def value(self):
		assert(self.number in self.NUMBERS)
		if self.number in self.VALUES:
			return self.VALUES[self.number]
		else:
			return 0
	
	def taking_power(self, leading_suit, trump_suit):
		power = self.NUMBERS.index(self.number)
		if self.suit == leading_suit:
			power = power + 10
		
		if self.suit == trump_suit:
			power = power + 20
	
	def __repr__(self):
		return self.number + self.suit
		
class Deck:
	def __init__(self):
		self.cards = []
		for suit in Card.SUITS:
			for number in Card.NUMBERS:
				self.cards.append(Card(number+suit))
			
	def reset(self):
		__init__(self)
		
	def shuffle(self,random):
		random.shuffle(self.cards)
	
	def draw(self):
		if len(self.cards) == 0:
			raise CardNotFound("Tried to draw, but deck was empty")
		return self.cards.pop(0)
		
	def size(self):
		return len(deck.cards)
		

	

class GameUpdateMessage:
	def __init__(self, player_id, message, options):
		self.player_id = player_id
		self.message = message
		self.options = options
		
	def __repr__(self):
		return "P" + str(self.player_id) + " << " +  self.message + "\n" + str(self.options)
		

