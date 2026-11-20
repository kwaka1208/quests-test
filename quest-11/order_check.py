"""Stage 3: Make the biggest order that the code allows.

Each item can be anything, like "salad". Change the list below, and run: python order_check.py
"""
from lunch_points import make_order

# ---- Edit this line ----
items = ["salad", "coffee"]

# ---- Do not edit below this line ----
import base64

try:
    order = make_order(items)
except ValueError as err:
    print(f"make_order() の返事: {err}。多すぎるようです。")
else:
    print(f"{len(items)} 個の注文は通りました。")
    if len(order["items"]) < 5:
        print("これがコードの受け付けるいちばん大きな注文ですか？ コメントだけでなく、コードで確かめましょう。")
    else:
        print("これがいちばん大きな注文です。本当のことを言うのはコードです！")
        print("答えになる単語:", base64.b64decode("dm91Y2hlcg==").decode())
