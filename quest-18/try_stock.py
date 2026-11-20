"""Daiki のコードを試します。このファイルは編集しないでください。実行: python try_stock.py"""
from stock import STOCK, report, take

print("Taking 10 salads:", take("salad", 10))
print("Taking 3 sandwiches:", take("sandwich", 3))
report()
