from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton




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