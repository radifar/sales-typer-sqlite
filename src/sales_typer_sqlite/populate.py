import datetime

from faker import Faker

from sales_typer_sqlite import database


fake = Faker()
Faker.seed(99)

connection = database.connect()
database.create_table(connection)

def populate_users(user_count: int = 15) -> None:
    users = []
    for _ in range(user_count):
        user = (fake.name(), fake.ascii_free_email())
        users.append(user)
    database.add_many_user(connection, users)

def populate_orders(order_count: int = 75, user_count: int = 15) -> None:
    orders = []
    products = 'modem pc monitor mouse keyboard router hdd ssd'.split()
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    for _ in range(order_count):
        order = (
            fake.random_element(products),
            fake.date_between(start_date, end_date),
            fake.random_int(min=1, max=user_count)
        )
        orders.append(order)
    orders.sort(key=lambda x: x[1])
    database.add_many_order(connection, orders)