<<<<<<< Updated upstream
from loader import updater
=======
# from loader import updater        # Будущий актуальный запуск
#
#
# if __name__ == '__main__':
#     updater.start_polling()
from config import config

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import contractor as ct

ROLE, FREELANCE_START, CUSTOMER_START, CUSTOMER_SUBSCRIBE, LOCATION, BIO = range(6)


def start(update, _):
    reply_keyboard = [['Я разработчик', 'Я заказчик']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        'Я - бот по организации PHP фрилансеров. '
        'Вы хотите быть фрилансером или заказчиком?\n\n'
        'Команда /cancel, чтобы прекратить разговор',
        reply_markup=markup_key
    )
    return ROLE


def freelance_menu(update, _):
    reply_keyboard = [['Помощь', 'Доступные заказы', 'Отчет']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        'Описание работы бота для фрилансера',
        reply_markup=markup_key
    )
    return FREELANCE_START


def freelance_get_orders(update, _):
    update.message.reply_text(
        'Вывод доступных заказов',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def freelance_get_report(update, _):
    update.message.reply_text(
        'Отчет по выполненным работам \n'
        f'{ct.fetch_completed_oreders()}',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def customer_menu(update, _):
    reply_keyboard = [['Оформить подписку', 'История заказов']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        'Здесь будет менюшка заказчика',
        reply_markup=markup_key,
    )
    return CUSTOMER_START


def customer_orders_history(update, _):
    update.message.reply_text(
        'Отчеты по выполненным и активным работам',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def subscribe(update, _):
    reply_keyboard = [['Согласен', 'Не согласен']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        'Условия подписки',
        reply_markup=markup_key,
    )
    return CUSTOMER_SUBSCRIBE


def customer_place_order(update, _):
    update.message.reply_text(
        'Размещение заказа',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def customer_declined(update, _):
    update.message.reply_text(
        'Прощание с клиентом',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
>>>>>>> Stashed changes


if __name__ == '__main__':
    updater.start_polling()
