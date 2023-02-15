# from loader import updater        # Будущий актуальный запуск
#
#
# if __name__ == '__main__':
#     updater.start_polling()
from telegram.error import BadRequest

from bot.keyboards.keyboard_factory import RoleSelectionInlineKeyboard, FreelancerMenuInlineKeyboard, \
    ConsentInlineKeyboard, CustomerMenuInlineKeyboard
from bot.states.start_states import States
from config import config

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler, CallbackContext,
)


def start(update: Update, context: CallbackContext):
    markup_key = InlineKeyboardMarkup(RoleSelectionInlineKeyboard().get_inline_keyboard())
    update.message.reply_text(
        'Я - бот по организации PHP фрилансеров. '
        'Вы хотите быть фрилансером или заказчиком?\n\n'
        'Команда /cancel, чтобы прекратить разговор',
        reply_markup=markup_key
    )
    return States.ROLE


def freelance_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    markup_key = InlineKeyboardMarkup(FreelancerMenuInlineKeyboard().get_inline_keyboard())
    try:
        query.edit_message_text(text='Описание работы бота для фрилансера',
                                reply_markup=markup_key)
    except BadRequest:
        query.edit_message_text('Описание работы бота для фрилансера (возможно более подробное)',
                                reply_markup=markup_key)
    return States.FREELANCE_START


def freelance_get_orders(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text='Вывод доступных заказов', reply_markup=None)

    return ConversationHandler.END


def freelance_get_report(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text='Отчет по выполненным работам', reply_markup=None)

    return ConversationHandler.END


def customer_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    markup_key = InlineKeyboardMarkup(CustomerMenuInlineKeyboard().get_inline_keyboard())
    query.edit_message_text(text='Здесь будет менюшка заказчика', reply_markup=markup_key)

    return States.CUSTOMER_START


def customer_orders_history(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text='Отчеты по выполненным и активным работам', reply_markup=None)

    return ConversationHandler.END


def subscribe(update: Update, context: CallbackContext):
    query = update.callback_query
    markup_key = InlineKeyboardMarkup(ConsentInlineKeyboard().get_inline_keyboard())
    query.edit_message_text(text='Условия подписки', reply_markup=markup_key)

    return States.CUSTOMER_SUBSCRIBE


def customer_place_order(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text='Размещение заказа', reply_markup=None)

    return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.',
        reply_markup=ReplyKeyboardRemove()
    )
def customer_declined(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text='Прощание с клиентом', reply_markup=None)

    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token=config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.ROLE:
                [
                    CallbackQueryHandler(freelance_menu, pattern='freelancer'),
                    CallbackQueryHandler(customer_menu, pattern='customer')
                ],
            States.FREELANCE_START:
                [
                    CallbackQueryHandler(freelance_menu, pattern='help'),
                    CallbackQueryHandler(freelance_get_orders, pattern='available_orders'),
                    CallbackQueryHandler(freelance_get_report, pattern='report')
                ],
            States.CUSTOMER_START:
                [
                    CallbackQueryHandler(subscribe, pattern='subscribe'),
                    CallbackQueryHandler(customer_orders_history, pattern='orders_history')
                ],
            States.CUSTOMER_SUBSCRIBE:
                [
                    CallbackQueryHandler(customer_place_order, pattern='agree'),
                    CallbackQueryHandler(customer_declined, pattern='disagree')
                ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
