import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	chat_id = Column(Integer, primary_key=True)
	name = Column(String)
	game = Column(Integer, ForeignKey("games.id"))
	player_id = Column(Integer)
	view = Column(String)
	
	def __init__(self, bot, chat_id, name):
		self.chat_id = chat_id
		self.name = name
		self.view = "MainMenu"

	def send_update(bot):
		bot.sendMessage(chat_id = self.chat_id, text = update.ita(self.player_id), ReplyKeyboardMarkup(update.options(self.player_id)))
		
