from loader import bot
from telebot.custom_filters import StateFilter


if __name__ == '__main__':
    from handlers import bot

    bot.add_custom_filter(StateFilter(bot))
    bot.polling(none_stop=True)
