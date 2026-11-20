"""The lunch kiosk of Northwind. A tiny app that shows the messages in messages.json.

Run: python kiosk.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRICES = {"sandwich": 5, "salad": 4, "coffee": 2, "cookie": 1}
TRAY_LIMIT = 3


def dollars(n):
    return f"{n} dollar" if n == 1 else f"{n} dollars"


def main():
    messages = json.loads((HERE / "messages.json").read_text(encoding="utf-8"))
    money = 10
    tray = []
    print("Welcome to the Northwind lunch kiosk! Type 'menu', 'order <item>', or 'quit'.")
    while True:
        print()
        command = input("> ").strip().lower()
        values = {"command": command, "item": "", "price": 0, "money": money, "limit": TRAY_LIMIT}
        if command == "":
            print("Please type a command.")
        elif command == "quit":
            print("See you tomorrow!")
            break
        elif command == "menu":
            for name, price in PRICES.items():
                print(f"  {name}: {dollars(price)}")
            print(f"You have {dollars(money)}. Your tray: {', '.join(tray) or 'empty'}")
        elif command.startswith("order "):
            item = command[6:].strip()
            values.update(item=item, price=PRICES.get(item, 0))
            if item not in PRICES:
                print(messages["unknown_item"].format(**values))
            elif item in tray:
                print(f"You already have a {item} on your tray.")
            elif len(tray) >= TRAY_LIMIT:
                print(f"Your tray is full ({TRAY_LIMIT} items).")
            elif PRICES[item] > money:
                print(messages["no_money"].format(**values))
            else:
                money -= PRICES[item]
                tray.append(item)
                print(f"You ordered a {item}. You have {dollars(money)} left.")
        else:
            print(messages["unknown_command"].format(**values))


if __name__ == "__main__":
    main()
