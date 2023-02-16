import math
from abc import ABC

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class ButtonFactory(ABC):
    def get_inline_keyboard(self):
        key_list = self.__dict__

        inline_keyboard = []

        for i_key in key_list.values():
            for j_key, j_value in i_key.items():
                inline_keyboard.append(
                    InlineKeyboardButton(
                        text=j_key, callback_data=j_value))                

        try:
            if len(inline_keyboard) == any(inline_keyboard_len for inline_keyboard_len in range(1, 4)):
                return inline_keyboard
        finally:
            if not any(isinstance(inline_keyboard, list) for _ in inline_keyboard):
                return inline_keyboard

        upd_inline_keyboard = []
        index = 0
        for _ in range(math.ceil(len(inline_keyboard) / 3)):
            upd_inline_keyboard.append(inline_keyboard[index:index + 3])
            index += 3
        return upd_inline_keyboard


class RoleSelectionInlineKeyboard(ButtonFactory):

    def __init__(self):
        self.developer = {'Я Разработчик': 'freelancer'}
        self.customer = {'Я заказчик': 'customer'}


class FreelancerMenuInlineKeyboard(ButtonFactory):

    def __init__(self):
        self.help = {'Помощь': 'help'}
        self.available_orders = {'Доступные заказы': 'freelance_order#1'}
        self.report = {'Отчет': 'report'}


class CustomerMenuInlineKeyboard(ButtonFactory):

    def __init__(self):
        self.subscribe = {'Оформить подписку': 'subscribe'}
        self.orders_history = {'История заказов': 'customer_order#1'}


class ConsentInlineKeyboard(ButtonFactory):

    def __init__(self):
        self.agree = {'Согласен': 'agree'}
        self.disagree = {'Не согласен': 'disagree'}


class ReturnFreelancerInlineKeyboard(ButtonFactory):

    def __init__(self):        
        self.return_state = {'Назад': 'freelancer1'}
        