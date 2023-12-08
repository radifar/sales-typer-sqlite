import sqlite3
import datetime


CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS Users(
            user_id INTEGER PRIMARY KEY,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Orders(
            order_id INTEGER PRIMARY KEY,
            order_product TEXT NOT NULL,
            order_date TEXT NOT NULL,
            user_id INTEGER REFERENCES Users
        );
"""

INSERT_USER = 'INSERT INTO Users (user_name, user_email) VALUES (?, ?);'
INSERT_ORDER = 'INSERT INTO Orders (order_product, order_date, user_id) VALUES (?, ?, ?);'

GET_ALL_USER = 'SELECT * FROM Users;'
GET_USER_BY_ID = 'SELECT * FROM Users WHERE user_id = ?;'
UPDATE_USER_EMAIL = 'UPDATE Users SET user_email = ? WHERE user_id = ?;'

GET_ALL_ORDER = 'SELECT * FROM Orders;'

TOTAL_ORDER_COUNT_BY_USER = """
        SELECT Orders.user_id, Users.user_name, Users.user_email, COUNT(Orders.user_id) AS total_order
        FROM Orders
        LEFT JOIN Users
        ON Orders.user_id = Users.user_id
        GROUP BY Orders.user_id;
"""

TOTAL_ORDER_COUNT_BY_USER_HIGHER = """
        SELECT Orders.user_id, Users.user_name, Users.user_email, COUNT(Orders.user_id) AS total_order
        FROM Orders
        LEFT JOIN Users
        ON Orders.user_id = Users.user_id
        GROUP BY Orders.user_id
        HAVING total_order > ?;
"""

TOTAL_ORDER_COUNT_BY_USER_LOWER = """
        SELECT Orders.user_id, Users.user_name, Users.user_email, COUNT(Orders.user_id) AS total_order
        FROM Orders
        LEFT JOIN Users
        ON Orders.user_id = Users.user_id
        GROUP BY Orders.user_id
        HAVING total_order < ?;
"""

MONTHLY_SALES = """
        SELECT strftime('%Y-%m', order_date) year_month, COUNT(*) total_sales
        FROM Orders
        GROUP BY year_month
"""

def adapt_date_iso(value: datetime.date):
    return value.isoformat()

def convert_date(value: str):
    return datetime.date.fromisoformat()

sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_converter("date", convert_date)

def connect(location: str = 'sales.db') -> sqlite3.Connection:
    return sqlite3.connect(location)

def create_table(connection: sqlite3.Connection):
    with connection:
        connection.executescript(CREATE_TABLE)

def add_user(connection: sqlite3.Connection, user: tuple):
    with connection:
        connection.execute(INSERT_USER, user)

def add_many_user(connection: sqlite3.Connection, users: list[tuple]):
    with connection:
        connection.executemany(INSERT_USER, users)

def get_user(connection: sqlite3.Connection, user_id: int) -> tuple:
    with connection:
        return connection.execute(GET_USER_BY_ID, (user_id,)).fetchone()

def get_all_user(connection: sqlite3.Connection) -> list[tuple]:
    with connection:
        return connection.execute(GET_ALL_USER).fetchall()

def update_user_email(connection: sqlite3.Connection, user_id: int, email: str):
    with connection:
        connection.execute(UPDATE_USER_EMAIL, (email, user_id))
        return connection.execute(GET_USER_BY_ID, (user_id,)).fetchone()

def add_order(connection: sqlite3.Connection, order: tuple):
    with connection:
        connection.execute(INSERT_ORDER, order)

def add_many_order(connection: sqlite3.Connection, orders: list[tuple]):
    with connection:
        connection.executemany(INSERT_ORDER, orders)

def get_all_order(connection: sqlite3.Connection) -> list[tuple]:
    with connection:
        return connection.execute(GET_ALL_ORDER).fetchall()

def calculate_total_order(connection: sqlite3.Connection) -> list[tuple]:
    with connection:
        return connection.execute(TOTAL_ORDER_COUNT_BY_USER).fetchall()

def calculate_total_order_higher(connection: sqlite3.Connection, value: int) -> list[tuple]:
    with connection:
        return connection.execute(TOTAL_ORDER_COUNT_BY_USER_HIGHER, (value,)).fetchall()

def calculate_total_order_lower(connection: sqlite3.Connection, value: int) -> list[tuple]:
    with connection:
        return connection.execute(TOTAL_ORDER_COUNT_BY_USER_LOWER, (value,)).fetchall()

def calculate_monthly_sales(connection:sqlite3.Connection) -> list[tuple]:
    with connection:
        return connection.execute(MONTHLY_SALES).fetchall()
