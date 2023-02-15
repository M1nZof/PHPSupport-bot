# from telebot.types import Message
from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id, "start")
