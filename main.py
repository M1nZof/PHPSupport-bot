from bot.config.config import secret_key
from bot.keyboards.keyboard_factory import RoleSelectionInlineKeyboard, FreelancerMenuInlineKeyboard, \
    ConsentInlineKeyboard, CustomerMenuInlineKeyboard, AdminMenuInlineKeyboard
from bot.keyboards.pagination import freelance_orders_page_callback, customer_orders_page_callback, \
    admin_orders_page_callback, admin_freelancers_page_callback, admin_customers_page_callback
from bot.states.start_states import States
from bot.config import config

from telegram.error import BadRequest

from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler, CallbackContext, MessageHandler, Filters
)
import bot.contractor as ct


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
    ct.get_free_works(context=context)
    ct.get_orders_in_progress(context)
    print(context.user_data['free_works'])
    return States.ROLE


def start1(update: Update, context: CallbackContext):  # TODO временное решение для демонстрации
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


def freelance_choice_order(update: Update, context: CallbackContext):
    ct.choice_order(update, context)

    return States.FREELANCE_CHOICE_ORDERS


def form_order(update: Update, context: CallbackContext):
    ct.form_freelance_order(update, context)
    return ConversationHandler.END


def freelance_get_report(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = ct.return_button('freelancer')
    # query.edit_message_text(text='Отчет по выполненным работам', reply_markup=reply_markup)

    query.edit_message_text(text=  # TODO реализовать позже
                            'Отчет по выполненным работам \n'
                            f'{ct.fetch_completed_orders(update, context)}',
                            reply_markup=reply_markup
                            )

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
    reply_markup = ct.return_button('back')
    query.edit_message_text(text='Размещение заказа', reply_markup=reply_markup)

    return ConversationHandler.END


def customer_declined(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text='Прощание с клиентом', reply_markup=None)

    return ConversationHandler.END


def init_admin(update: Update, context: CallbackContext):
    update.message.reply_text(text='Пожалуйста, введите код доступа к панели управления',
                              reply_markup=None)

    return States.ADMIN_START


def wrong_admin(update: Update, context: CallbackContext):
    pass


def admin_menu(update: Update, context: CallbackContext):
    markup_key = InlineKeyboardMarkup(AdminMenuInlineKeyboard().get_inline_keyboard())
    try:
        update.message.reply_text(text='<b>Меню администратора</b>\n\n'
                                       'Пожалуйста, выберите категорию',
                                  reply_markup=markup_key,
                                  parse_mode='HTML')
    except AttributeError:
        query = update.callback_query
        query.edit_message_text(text='<b>Меню администратора</b>\n\n'
                                     'Пожалуйста, выберите категорию',
                                reply_markup=markup_key,
                                parse_mode='HTML')

    return States.ADMIN_MENU


def admin_orders(update: Update, context: CallbackContext):
    admin_orders_page_callback(update, context)

    return States.ADMIN_ORDERS


def admin_customers(update: Update, context: CallbackContext):
    admin_customers_page_callback(update, context)

    return States.ADMIN_CUSTOMERS


def admin_freelancers(update: Update, context: CallbackContext):
    admin_freelancers_page_callback(update, context)

    return States.ADMIN_FREELANCERS


def stop(update: Update, context: CallbackContext):
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token=config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    work_area = ConversationHandler(
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
                    CallbackQueryHandler(start1, pattern='main_menu'),
                    CallbackQueryHandler(freelance_menu, pattern='freelancer'),

                    # TODO временное решение для демонстрации
                ],
            States.FREELANCE_ORDERS:
                [
                    CallbackQueryHandler(freelance_orders_page_callback, pattern='^freelance_order#'),
                    CallbackQueryHandler(freelance_menu, pattern='freelancer'),
                    CallbackQueryHandler(freelance_menu, pattern='back'),
                    CallbackQueryHandler(freelance_choice_order, pattern='get_order'),

                ],
            States.CUSTOMER_START:
                [
                    CallbackQueryHandler(subscribe, pattern='subscribe'),
                    CallbackQueryHandler(customer_orders_history, pattern='customer_order#1'),
                    CallbackQueryHandler(start1, pattern='main_menu')
                ],

            States.CUSTOMER_SUBSCRIBE:
                [
                    CallbackQueryHandler(customer_place_order, pattern='agree'),
                    CallbackQueryHandler(customer_declined, pattern='disagree'),
                ],
            States.CUSTOMER_ORDERS:
                [
                    CallbackQueryHandler(customer_orders_page_callback, pattern='^customer_order#'),
                    CallbackQueryHandler(customer_menu, pattern='back')
                ],
            States.FREELANCE_CHOICE_ORDERS:
                [
                    MessageHandler(
                        Filters.text, form_order
                    ),
                ]
        },
        fallbacks=[
            CommandHandler('rerun', start),
            CommandHandler('stop', stop)
        ],
    )

    admin_area = ConversationHandler(
        entry_points=[CommandHandler('admin', init_admin)],
        states={
            States.ADMIN_START:
                [
                    MessageHandler(Filters.text(secret_key), admin_menu),
                    MessageHandler(Filters.text, wrong_admin)
                ],
            States.ADMIN_MENU:
                [
                    CallbackQueryHandler(admin_orders, pattern='^admin_orders#'),
                    CallbackQueryHandler(admin_customers, pattern='^admin_customers#'),
                    CallbackQueryHandler(admin_freelancers, pattern='^admin_freelancers#')
                ],
            States.ADMIN_CUSTOMERS:
                [
                    CallbackQueryHandler(admin_customers_page_callback, pattern='^admin_customers#'),
                    CallbackQueryHandler(admin_menu, pattern='back')
                ],
            States.ADMIN_FREELANCERS:
                [
                    CallbackQueryHandler(admin_freelancers_page_callback, pattern='^admin_freelancers#'),
                    CallbackQueryHandler(admin_menu, pattern='back')
                ]
        },
        fallbacks=[
            CommandHandler('admin', init_admin),
            CommandHandler('stop', stop)
        ]
    )

    dispatcher.add_handler(work_area)
    dispatcher.add_handler(admin_area)

    updater.start_polling()
    updater.idle()
