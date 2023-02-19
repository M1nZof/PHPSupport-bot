from telegram import Update, InlineKeyboardButton
from telegram.ext import CallbackContext
from telegram_bot_pagination import InlineKeyboardPaginator


orders_example = [f"{order_index} заказ" for order_index in range(1, 10)]


# def freelance_available_orders(update: Update, context: CallbackContext):     # Пока оставлю. Может еще пригодится
#     paginator = InlineKeyboardPaginator(
#         len(orders_example),        # TODO изменить на данные из базы
#         data_pattern='freelance_order#{page}'
#     )
#
#     update.message.reply_text(
#         text=orders_example[0],     # TODO изменить на данные из базы + форматирование
#         reply_markup=paginator.markup,
#         parse_mode='Markdown'
#     )


def freelance_orders_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        context.user_data['num_free_works'],        # TODO изменить на данные из базы
        current_page=page,
        data_pattern='freelance_order#{page}'
    )

    paginator.add_before(InlineKeyboardButton('Взять заказ', callback_data='get_order'))
    paginator.add_after(InlineKeyboardButton('Вернуться в меню', callback_data='back'))
    # TODO прописать возвращение в freelance menu

    context.user_data['num_order'] = page-1
    query.edit_message_text(
        text=context.user_data['free_works']['Описание'][page-1],  # TODO изменить на данные из базы + форматирование
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


# def customer_available_orders(update: Update, context: CallbackContext):  # Пока оставлю. Может еще пригодится
#     paginator = InlineKeyboardPaginator(
#         len(orders_example),        # TODO изменить на данные из базы
#         data_pattern='customer_order#{page}'
#     )
#
#     update.message.reply_text(
#         text=orders_example[0],     # TODO изменить на данные из базы + форматирование
#         reply_markup=paginator.markup,
#         parse_mode='Markdown'
#     )


def customer_orders_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        len(orders_example),        # TODO изменить на данные из базы
        current_page=page,
        data_pattern='customer_order#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Вернуться в меню', callback_data='back'))
    # TODO прописать возвращение в freelance menu

    query.edit_message_text(
        text=orders_example[page - 1],  # TODO изменить на данные из базы + форматирование
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


def admin_orders_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        len(orders_example),  # TODO изменить на данные из базы
        current_page=page,
        data_pattern='admin_orders#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Вернуться в меню', callback_data='back'))
    # TODO прописать возвращение в admin menu

    query.edit_message_text(
        text=orders_example[page - 1],  # TODO изменить на данные из базы + форматирование
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


def admin_customers_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        len(orders_example),  # TODO изменить на данные из базы
        current_page=page,
        data_pattern='admin_customers#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Вернуться в меню', callback_data='back'))
    # TODO прописать возвращение в admin menu

    query.edit_message_text(
        text=orders_example[page - 1],  # TODO изменить на данные из базы + форматирование
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


def admin_freelancers_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        len(orders_example),  # TODO изменить на данные из базы
        current_page=page,
        data_pattern='admin_freelancers#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Вернуться в меню', callback_data='back'))
    # TODO прописать возвращение в admin menu

    query.edit_message_text(
        text=orders_example[page - 1],  # TODO изменить на данные из базы + форматирование
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
