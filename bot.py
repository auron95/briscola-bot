#!/usr/bin/python

# Lo script viene eseguito con due parametri:
# Il primo e` l'update Telegram sotto forma di json
# Il secondo e` il token

import sys
import json
# Aggiunge il pacchetto python-telegram-bot installato in locale
sys.path.insert(0, 'python-telegram-bot')
import telegram 

def handle_update (update, bot):
	chat_id = update.message.chat.id
	text = update.message.text.encode('utf-8')
	bot.sendMessage(chat_id=chat_id, text=text)

if __name__ == "__main__":
	bot = telegram.Bot(token=sys.argv[2])
	update = telegram.Update.de_json(json.loads(sys.argv[1]),bot)
	handle_update (update, bot)
