"""The menu of Northwind Lunch. The functions work, but they have no docstrings.

Write a docstring for each function. Do not change the code.
"""

MENU = {"sandwich": 5.0, "salad": 4.0, "coffee": 2.0, "cookie": 1.0}  # prices in dollars


def total_price(items, tax_rate=0.1):
    total = sum(MENU[name] for name in items)
    return round(total * (1 + tax_rate), 2)


def find_item(name):
    key = name.strip().lower()
    if key not in MENU:
        raise KeyError(f"there is no item called {name!r}")
    return MENU[key]


def print_menu():
    for name, price in MENU.items():
        print(f"{name}: ${price:.2f}")
