from errors import *

class Player:
	def __init__ (self, game, index, name = None):
		self.index = index
		self.name = name or "Player " + str(index)
		self.last_message = None
		self.game = game
		self.hand = CardCollection()
		self.collected_points = 0
		self.overall_points = 0
		self.collected_cards = CardCollection()
	
	def __repr__(self):
		return str(self.name) + "(Giocatore " + str(self.index) + ")"
		
	def next(self):
		assert(self.game.players[self.index] == self)
		return self.game.players[self.index - len(self.game.players) + 1]
		
	def draw(self, deck, num=1):
		drawn = deck.draw(num)
		self.hand.cards += drawn.cards
		return drawn
	
	
	def play(self,card):
		index = self.hand.card_index(card)
		if index==None:
			raise IllegalMove(str(self) + " tried to play " + str(card) + " but that he had " + str(self.hand) + " in his hand.")
		else:
			self.game.field.plays.append((self, self.hand.cards.pop(index)))
			assert(self.hand.card_index(card)==None)
			
class Field:
	def __init__(self):
		self.plays = []
		
	def get_leading_suit(self):
		if len(self.plays) == 0:
			return None
		else:
			return self.plays[0][1].suit
			
	def clear(self):
		self.__init__()

	def get_taking_play(self, trump = None):
		return max(self.plays, key=lambda p: p[1].taking_power(self.plays[0][1].suit, trump))
		
	def points_on_the_field(self):
		return self.cards().value()
		
	def cards(self):
		return CardCollection([ card for p, card in self.plays ])
		
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
		"3": 10,
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
			
		return power
	
	def __str__(self):
		try:
			return str(self.number) + self.suit
		except UnicodeDecodeError:
			print self.number + self.suit
			raise
		
class CardCollection:
	
	def __init__(self, cards = None):
		self.cards = cards or []
			
	def reset(self):
		__init__(self)
		
	def card_index(self,card):
		# Check if player has a card, and return that if found
		matches = [i for i, c in enumerate(self.cards) if str(c) == str(card)]
		assert(len(matches)<=1)
		if len(matches) == 0:
			return None
		else:
			return matches[0]

	def shuffle(self,random):
		random.shuffle(self.cards)
	
	def draw(self, num = 1):
		if self.size() < num:
			raise CardNotFound("Tried to draw " + str(num) + " cards, but deck had only " + str(len(self.cards)) + ".")
		drawn = self.cards[:num]
		del self.cards[:num]
		return CardCollection(drawn)
		
	def size(self):
		return len(self.cards)
	
	def value(self):
		return sum(map(lambda card: card.value(),self.cards))
		
	def __str__(self):
		return " ".join(str(card) for card in self.cards)
		
	def __repr__(self):
		return "Deck: << " + " ".join(str(card) for card in self.cards)

class Deck(CardCollection):
	def __init__(self, Card):
		self.cards = []
		for suit in Card.SUITS:
			for number in Card.NUMBERS:
				self.cards.append(Card(number+suit))
	
class Dispatcher:
	def __init__(self, game):
		self.game = game
		
	def dispatch_game_updates(self, updates):
		for update in updates:
			self.output(update) 
		
	def output(self, update, player_id):
		raise NotImplementedError('Output not implemented')

	def input(self, input_msg):
		raise NotImplementedError('Input not implemented')

