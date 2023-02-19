from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton
import pandas as pd
from telegram.ext import CallbackContext
from datetime import date


def get_free_works(context: CallbackContext):

    free_works = pd.read_csv('works_free.csv', header=0, encoding='cp1251', delimiter=';')
    context.user_data['free_works'] = free_works.to_dict()
    context.user_data['num_free_works'] = free_works.shape[0]
    

def get_orders_in_progress(context: CallbackContext):
    orders_in_progress = pd.read_csv('orders_in_progress.csv', header=0, encoding='cp1251', delimiter=';')
    context.user_data['orders_in_progres'] = orders_in_progress

def fetch_completed_orders():
    completed_orders = [
        {
            'id': 151,
            'id_customer': 25,
            'id_contractor': 737812092,
            'description': 'Добавить платёжную систему на сайт',
            'completed': True,
            'in_work': True,
            'cost': 1500.00
        },
        {
            'id': 155,
            'id_customer': 25,
            'id_contractor': 737812092,
            'description': 'выгрузить товары с сайта в Excel-таблице',
            'completed': True,
            'in_work': True,
            'cost': 1500.00
        },
        {
            'id': 159,
            'id_customer': 26,
            'id_contractor': 737812092,
            'description': 'загрузить 450 SKU на сайт из Excel таблицыт',
            'completed': True,
            'in_work': True,
            'cost': 1500.00
        },
        {
            'id': 161,
            'id_customer': 22,
            'id_contractor': 737812092,
            'description': 'разместить баннер',
            'completed': True,
            'in_work': True,
            'cost': 1500.00
        },
        {
            'id': 171,
            'id_customer': 29,
            'id_contractor': 737812092,
            'description': 'добавить платёжную систему на сайт',
            'completed': True,
            'in_work': True,
            'cost': 1500.00
        },
        {
            'id': 191,
            'id_customer': 27,
            'id_contractor': 737812092,
            'description': 'добавить в интернет-магазин фильтр товаров по цвету',
            'completed': True,
            'in_work': True,
            'cost': 1500.00
        },
        {
            'id': 195,
            'id_customer': 29,
            'id_contractor': 737812092,
            'description': 'добавить в интернет-магазин фильтр товаров по цвету',
            'completed': True,
            'in_work': True,
            'cost': 1500.00
        },
    ]
    orders_to_message = list()
    total_cost = 0
    for order in completed_orders:
        orders_to_message.append(
            f'описание: {order["description"]}, оплата: {order["cost"]} \n'
        )
        total_cost += order['cost']
    orders_to_message.append(
        f'Общая сумма: {total_cost} \n'
    )
    return ''.join(orders_to_message)
# print(fetch_completed_oreders())


def return_button(callback_action, name='Назад'):
    keyboard = [
        [
            InlineKeyboardButton(name, callback_data=callback_action),            
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def choice_order(update: Update, context: CallbackContext):

    query = update.callback_query    
    num_order = context.user_data["num_order"]
    message = f"Выбран заказ: {context.user_data['free_works']['Описание'][num_order]}\
    Введите расчётное время выполнения заказа"
    query.edit_message_text(text=message)
   
    
        
def form_freelance_order(update: Update, context: CallbackContext):    
    
    cost_per_order = 1500
    context.user_data["estimate"] = update.message.text
    update.message.reply_text('Информацияя о том, что заказ в работе, '
                              'передана заказчику')
    id_freelance = update['message']['chat']['id']
    order_in_progress = list()
    for free_works in context.user_data['free_works'].values():
        order_in_progress.append(free_works[context.user_data['num_order']])
    order_in_progress.append(id_freelance)
    order_in_progress.append(f'{date.today()}')
    order_in_progress.append(context.user_data["estimate"])
    order_in_progress.append(cost_per_order)
    context.user_data['orders_in_progres'].loc[ len(context.user_data['orders_in_progres'].index )] = order_in_progress
    context.user_data['orders_in_progres'].to_csv('orders_in_progress.csv', index=False, encoding='cp1251', delimiter=';')
    print(context.user_data["estimate"])
    print(context.user_data['orders_in_progres'])
