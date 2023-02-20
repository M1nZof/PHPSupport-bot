from peewee import (
    Model,
    CharField,
    SqliteDatabase,
    BooleanField,
    IntegerField,
    ForeignKeyField, TextField
)

db = SqliteDatabase("db6.sqlite3")


class Client(Model):
    telegram_id = IntegerField()
    full_name = CharField()
    is_subscribed = BooleanField(default=False)

    class Meta:
        database = db

    def __str__(self):
        return f'{self.fullname}'


class Freelancer(Model):
    telegram_id = IntegerField()
    full_name = CharField()
    # executed_orders = ArrayField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.fullname}'


class Order(Model):
    description = CharField()
    completed = BooleanField()
    in_work = BooleanField()
    client = ForeignKeyField(Client, field=Client.telegram_id, related_name='client_order')
    freelancer = ForeignKeyField(Freelancer, field=Freelancer.telegram_id, related_name='freelancer_order')

    class Meta:
        database = db

    def __str__(self):
        return f'{self.description}'


class Question(Model):
    order = ForeignKeyField(Order, field=Order.description, related_name='order_question')
    text = TextField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.text}'


# def create_tables():
#     with db:
#         # db.create_tables([Client, Freelancer, Order, Question])
#         db.create_tables(Client)


def initialize_db():
    db.connect()
    db.create_tables([Client, Freelancer, Order, Question], safe=True)
    db.close()
