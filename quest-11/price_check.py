"""Stage 1: How many points does a 5-dollar lunch give?

Read the docstring of points_for() in lunch_points.py, and set price below.
Then run: python price_check.py
"""
from lunch_points import points_for

# ---- Edit this line: the price of a 5-dollar lunch ----
price = 500

# ---- Do not edit below this line ----
import base64

points = points_for(price)
print(f"points_for({price}) = {points}")
if price != 5:
    print(f"ランチ1回で {points} ポイント？ 多すぎます。docstring で、price の単位を確かめましょう。")
else:
    print("正解！ それが正しい呼び出し方です。")
    print("（そう、5ドルでたった2ポイント。これが「ポイントの謎」です。FIXME に気づきましたか？）")
    print("答えになる単語:", base64.b64decode("cmVjZWlwdA==").decode())
