import matplotlib.pyplot as plt

def monthly_sales(data: list[tuple]) -> None:
    plt.plot(*zip(*data))

    plt.xlabel("Year Month")
    plt.ylabel("Total Sales")
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)

    plt.savefig('monthly_sales.png')
