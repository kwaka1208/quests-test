"""Prints a receipt. It was written for v1, and the total looks strange.

Fix it in the way that the team decided in devlog.md. Then run: python receipt.py
"""

# ---- Edit this part: the prices of a coffee and a salad (1.10 and 2.20 dollars) ----
PRICES = [1.1, 2.2]
# ---- Do not edit below this line ----

import base64
import decimal

total = sum(PRICES)
print("Prices:", PRICES)
print("Total: ", total)
if any(isinstance(p, decimal.Decimal) for p in PRICES):
    print("まだです: チームは Decimal を検討しましたが、選びませんでした。devlog.md の 'The decision' を読みましょう。")
elif any(isinstance(p, float) for p in PRICES):
    print("まだです: この合計は正しいですか？ devlog.md の 'The problem' と 'The decision' を読みましょう。")
elif total != 330:
    print("まだです: コーヒーは1.10ドル、サラダは2.20ドルです。チームが選んだ単位で書いてください。")
else:
    print(f"On the screen: {total // 100}.{total % 100:02d} dollars")
    print("正解！ もう丸めの誤差は出ません。")
    print("Code word:", base64.b64decode("bGVkZ2Vy").decode())
