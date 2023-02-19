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

def fetch_completed_orders(update: Update, context: CallbackContext):
    completed_orders = pd.read_csv('completed_orders.csv', header=0, encoding='cp1251', delimiter=';', index_col=0)
    # id_freelance = update['message']['chat']['id']
    # print(id_freelance)
    completed_orders = completed_orders[['Описание', 'Стоимость']]
    orders_to_message=list()
    total_cost = 0
    for _, order in completed_orders.iterrows():
        print(order)
        orders_to_message.append(
            f"Описание: {order['Описание']}; Стоимость: {order['Стоимость']} \n"
        )
        total_cost += order["Стоимость"]
    orders_to_message.append(
        f'Общая сумма: {total_cost} \n'
    )
    return ''.join(orders_to_message)
    # return completed_orders[['Описание', 'Стоимость']].to_dict()
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
