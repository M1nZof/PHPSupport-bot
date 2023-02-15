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
        'Отчет по выполненным работам',
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


if __name__ == '__main__':
    updater = Updater(token=config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ROLE:
                [
                    MessageHandler(Filters.text('Я разработчик'), freelance_menu),
                    MessageHandler(Filters.text('Я заказчик'), customer_menu)
                ],
            FREELANCE_START:
                [
                    MessageHandler(Filters.text('Помощь'), freelance_menu),
                    MessageHandler(Filters.text('Доступные заказы'), freelance_get_orders),
                    MessageHandler(Filters.text('Отчет'), freelance_get_report)
                ],
            CUSTOMER_START:
                [
                    MessageHandler(Filters.text('Оформить подписку'), subscribe),
                    MessageHandler(Filters.text('История заказов'), customer_orders_history)
                ],
            CUSTOMER_SUBSCRIBE:
                [
                    MessageHandler(Filters.text('Согласен'), customer_place_order),
                    MessageHandler(Filters.text('Не согласен'), customer_declined)
                ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
