#!/usr/bin/python

# Lo script viene eseguito con due parametri:
# Il primo e` l'update Telegram sotto forma di json
# Il secondo e` il token

import sys
import json
# Aggiunge il pacchetto python-telegram-bot installato in locale
import telegram
import game_utils
from users import User
import importlib
from game.database import Session

def handle_update (update, bot):
	session = Session()
	user = session.query(User).filter_by(chat_id = update.message.chat.id).first()
	if user is None:
		user = User(update.message.chat.id, "Test")
	View = getattr(importlib.import_module("views"), user.view)
	view = View(user, bot)
	view.send_input(update.message.text.encode('utf-8'))

if __name__ == "__main__":
	bot = telegram.Bot(token=sys.argv[2])
	update = telegram.Update.de_json(json.loads(sys.argv[1]),bot)
	handle_update (update, bot)
