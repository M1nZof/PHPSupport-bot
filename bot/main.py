from telegram.error import BadRequest

from keyboards.keyboard_factory import RoleSelectionInlineKeyboard, FreelancerMenuInlineKeyboard, \
    ConsentInlineKeyboard, CustomerMenuInlineKeyboard
from bot.keyboards.pagination import freelance_orders_page_callback, customer_orders_page_callback
from states.start_states import States
from config import config

from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler, CallbackContext,
)
import contractor as ct


# from loader import updater        # Будущий актуальный запуск
#
#
# if __name__ == '__main__':
#     updater.start_polling()


def start(update: Update, context: CallbackContext):
    markup_key = InlineKeyboardMarkup(RoleSelectionInlineKeyboard().get_inline_keyboard())
    update.message.reply_text(
        'Я - бот по организации PHP фрилансеров. '
        'Вы фрилансер или заказчик?',
        reply_markup=markup_key
    )
    return States.ROLE


def start1(update: Update, context: CallbackContext):       # TODO временное решение для демонстрации
    query = update.callback_query
    markup_key = InlineKeyboardMarkup(RoleSelectionInlineKeyboard().get_inline_keyboard())
    query.edit_message_text(
        text='Я - бот по организации PHP фрилансеров. '
        'Вы фрилансер или заказчик?',
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
    freelance_orders_page_callback(update, context)

    return States.FREELANCE_ORDERS


def freelance_get_report(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = ct.return_button('freelancer')
    query.edit_message_text(text='Отчет по выполненным работам', reply_markup=reply_markup)

    # update.message.reply_text(            # TODO реализовать позже
    #    'Отчет по выполненным работам \n'
    #    f'{ct.fetch_completed_orders()}',
    #    reply_markup=ReplyKeyboardRemove()
    # )   

    return States.FREELANCE_START


def customer_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    markup_key = InlineKeyboardMarkup(CustomerMenuInlineKeyboard().get_inline_keyboard())
    query.edit_message_text(text='Здесь будет менюшка заказчика', reply_markup=markup_key)

    return States.CUSTOMER_START


def customer_orders_history(update: Update, context: CallbackContext):
    customer_orders_page_callback(update, context)

    return States.CUSTOMER_ORDERS


def subscribe(update: Update, context: CallbackContext):
    query = update.callback_query
    markup_key = InlineKeyboardMarkup(ConsentInlineKeyboard().get_inline_keyboard())
    query.edit_message_text(text='Условия подписки', reply_markup=markup_key)

    return States.CUSTOMER_SUBSCRIBE


def customer_place_order(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text='Размещение заказа', reply_markup=None)

    return ConversationHandler.END


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
                    CallbackQueryHandler(customer_menu, pattern='customer'),
                ],
            States.FREELANCE_START:
                [
                    CallbackQueryHandler(freelance_menu, pattern='help'),
                    CallbackQueryHandler(freelance_get_orders, pattern='freelance_order#1'),
                    CallbackQueryHandler(freelance_get_report, pattern='report'),
                    CallbackQueryHandler(start1, pattern='main_menu'),      # TODO временное решение для демонстрации
                ],
            States.FREELANCE_ORDERS:
                [
                    CallbackQueryHandler(freelance_orders_page_callback, pattern='^freelance_order#'),
                    CallbackQueryHandler(freelance_menu, pattern='back')
                ],
            States.CUSTOMER_START:
                [
                    CallbackQueryHandler(subscribe, pattern='subscribe'),
                    CallbackQueryHandler(customer_orders_history, pattern='customer_order#1')
                ],
            States.CUSTOMER_SUBSCRIBE:
                [
                    CallbackQueryHandler(customer_place_order, pattern='agree'),
                    CallbackQueryHandler(customer_declined, pattern='disagree')
                ],
            States.CUSTOMER_ORDERS:
                [
                    CallbackQueryHandler(customer_orders_page_callback, pattern='^customer_order#')
                ]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
