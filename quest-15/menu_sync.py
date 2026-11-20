# Syncs today's menu to the lunch app. Written by Daiki for kitchen 2.x.
# Fix this file, and run: python menu_sync.py
import kitchen

menu = kitchen.get_menu()
for name, price in menu.items():
    print(name, price)
