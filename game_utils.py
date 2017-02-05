from errors import *

class Player:
	def __init__ (self, game, index, name = None, chat_id= None):
		self.chat_id = chat_id
		self.index = index
		self.name = name or "Player " + str(index)
		self.last_message = None
		self.game = game
		self.hand = []
		self.current_points = 0
		self.overall_points = 0
		self.collected_cards = []
	
	def __repr__(self):
		return str(self.name) + "(Giocatore " + str(self.index) + ")"
		
	def next(self):
		assert(self.game.players[self.index] == self)
		return self.game.players[self.index - len(self.game.players) + 1]
		
	def draw(self, deck, num=1):
		drawn = deck.draw(num)
		self.hand += drawn
		return drawn
	
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
			raise IllegalMove(str(self) + " tried to play " + str(card) + " but that he had " + str(self.hand) + " in his hand.")
		else:
			self.game.field.plays.append((self, self.hand.pop(index)))
			assert(self.card_index(card)==None)
			
class Field:
	def __init__(self):
		self.plays = []
		
	def get_leading_suit(self):
		if len(self.plays) == 0:
			return None
		else:
			return self.plays[0][1].suit

	def get_taking_play(self):
		return max(self.plays, lambda p: p[1].taking_power())
		
	def points_on_the_field(self):
		return sum(map(lambda card: card.value,self.cards()))
		
	def cards(self):
		return [ card for p, card in self.plays ]
		
	def to_string(expected_player = None):
		return ' '.join(str(card) for card in self.cards())
 
	
class Card:
	NUMBERS = ["2","4","5","6","7","J","Q","K","3","A"];
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
	
	def __str__(self):
		return self.number + self.suit
		
class Deck:
	def __init__(self, Card):
		self.cards = []
		for suit in Card.SUITS:
			for number in Card.NUMBERS:
				self.cards.append(Card(number+suit))
			
	def reset(self):
		__init__(self)
		
	def shuffle(self,random):
		random.shuffle(self.cards)
	
	def draw(self, num = 1):
		if len(self.cards) < num:
			raise CardNotFound("Tried to draw " + str(num) + " cards, but deck had only " + len(self.cards) + ".")
		drawn = self.cards[:num]
		del self.cards[:num]
		return drawn
		
	def size(self):
		return len(self.cards)
		
	def __repr__(self):
		return "Deck: << " + " ".join(str(card) for card in self.cards)
	

class GameUpdateMessage:
	def __init__(self, player, message, options):
		self.player = player
		self.message = message
		self.options = options
		
	def __repr__(self):
		return str(self.player) + " << " +  self.message + "\n" + str([str(opt) for opt in self.options])
		

