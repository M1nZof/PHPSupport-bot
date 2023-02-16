from django.db import models
from django.core.validators import MinValueValidator


class Contractor(models.Model):
    """Подрядчик"""
    telegram_id = models.IntegerField(
        verbose_name='Телеграм ID юзера'
    )
    fullname = models.CharField(
        max_length=30,
        verbose_name='Имя и фамилия пользователя'
    )

    class Meta:
        db_table = 'contractor'
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'

    def __str__(self):
        return f'{self.fullname}'


class Client(models.Model):
    """Клиент, который оплатил подписку"""
    telegram_id = models.IntegerField(
        verbose_name='Телеграм ID юзера'
    )
    fullname = models.CharField(
        max_length=30,
        verbose_name='Имя и фамилия пользователя'
    )
    is_subscripted = models.BooleanField(
        verbose_name='Оплатил подписку',
        default=False,
    )

    class Meta:
        db_table = 'client'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.fullname}'


class Task(models.Model):
    """Задание"""
    description = models.TextField(
        verbose_name='Описание задачи',
    )
    completed = models.BooleanField(
        verbose_name='Выполнена',
        default=False,
    )
    in_work = models.BooleanField(
        verbose_name='В работе',
        default=False,
    )
    cost = models.IntegerField(
        verbose_name='Стоимость',
    )
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        related_name='tasks',
        on_delete=models.PROTECT,
    )
    contractor = models.ForeignKey(
        Contractor,
        verbose_name='Заказчик',
        related_name='tasks',
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        db_table = 'task'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.description}'


class Question(models.Model):
    task = models.ForeignKey(
        Task,
        verbose_name='Заявка',
        related_name='questions',
        on_delete=models.PROTECT
    )
    text = models.TextField(
        verbose_name='Текст вопроса'
    )

    class Meta:
        db_table = 'question'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.text}'
