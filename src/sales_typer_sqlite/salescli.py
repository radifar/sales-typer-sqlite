import datetime

import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table

from sales_typer_sqlite import charts, database, populate


console = Console()
app = typer.Typer()

connection = database.connect()
database.create_table(connection)

def rich_user_table() -> Table:
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", width=6)
    table.add_column("Name", min_width=20)
    table.add_column("Email", min_width=12)

    return table

def rich_order_table() -> Table:
    table = Table(show_header=True, header_style="bold orange_red1")
    table.add_column("ID", width=6)
    table.add_column("Product", min_width=12)
    table.add_column("Date", width=12)
    table.add_column("User ID", width=8)

    return table

@app.command(short_help="add user")
def adduser(name: str, email: str):
    typer.echo(f'Adding user with name: "{name}" and email address: "{email}"')
    user = (name, email)
    database.add_user(connection, user)
    showalluser()

@app.command(short_help="show all user")
def showalluser():
    users = database.get_all_user(connection)
    console.print("[bold magenta]Users[/bold magenta]", "🧑")

    table = rich_user_table()

    for user in users:
        table.add_row(str(user[0]), user[1], user[2])
    
    console.print(table)

@app.command(short_help="update user email with the given user_id")
def updateuseremail(user_id: int, email: str):
    typer.echo(f'Updating user email with user_id {user_id} as {email}')
    database.update_user_email(connection, user_id, email)
    user = database.get_user(connection, user_id)

    table = rich_user_table()
    table.add_row(str(user[0]), user[1], user[2])

    console.print(table)

@app.command(short_help="add order")
def addorder(product: str, date: str, user_id: int):
    typer.echo(f'adding order with {product} at {date} by user with user_id {user_id}')
    date = datetime.date.fromisoformat(date)
    order = (product, date, user_id)
    database.add_order(connection, order)
    showallorder()

@app.command(short_help="display all orders")
def showallorder():
    console.print("[bold orange_red1]Orders[/bold orange_red1]", "🛒")

    orders = database.get_all_order(connection)
    table = rich_order_table()

    for order in orders:
        table.add_row(str(order[0]), order[1], order[2], str(order[3]))
    
    console.print(table)

@app.command(short_help="calculate total order for each user")
def totalorder(
    higher_than: Annotated[int, typer.Option(help="Filter total order higher than provided value")] = 0,
    lower_than: Annotated[int, typer.Option(help="Filter total order lower than provided value")] = 0,
):
    if higher_than:
        typer.echo(f'Total amount of order for each user where total amount higher than {higher_than}')
        total_order = database.calculate_total_order_higher(connection, higher_than)
    elif lower_than:
        typer.echo(f'Total amount of order for each user where total amount lower than {lower_than}')
        total_order = database.calculate_total_order_lower(connection, lower_than)
    else:
        typer.echo(f'Total amount of order for each user')
        total_order = database.calculate_total_order(connection)
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", width=6)
    table.add_column("Name", min_width=20)
    table.add_column("Email", min_width=12)
    table.add_column("total order", width=14)

    for user in total_order:
        table.add_row(str(user[0]), user[1], user[2], str(user[3]))
    
    console.print(table)

@app.command(short_help="show monthly sales trend and save it as monthly_sales.png")
def monthlysales():
    typer.echo('Sales trend generated as monthly_sales.png')
    sales = database.calculate_monthly_sales(connection)
    charts.monthly_sales(sales)

@app.command(short_help="populate users and orders table")
def populatetable():
    typer.echo('populate the users and orders table')
    populate.populate_users()
    populate.populate_orders()

if __name__ == "__main__":
    app()