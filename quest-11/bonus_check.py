"""Stage 2: Give the Friday bonus to a customer with 5 points.

old_bonus() does not work anymore. Read the docstrings and the comments in lunch_points.py,
and change the line below. Then run: python bonus_check.py
"""
from lunch_points import *  # noqa: F401,F403

# ---- Edit this line ----
total = old_bonus(5)

# ---- Do not edit below this line ----
import base64

print(f"total = {total}")
if total == 10:
    print("正解！ 金曜日はポイントが2倍になりました。")
    print("答えになる単語:", base64.b64decode("dGlja2V0").decode())
elif total == 5:
    print("ボーナスがつきません。今日は金曜日です。docstring で、曜日の書き方を確かめましょう。")
else:
    print(f"{total} ポイント？ 多すぎます。使った関数のコメント（TODO や FIXME）を読みましょう。")
