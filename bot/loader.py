from telegram.ext import CommandHandler, Updater

from bot.handlers.start import start
from config import config


updater = Updater(token=config.BOT_TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
