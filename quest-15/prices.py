"""Prices of Northwind Lunch. Fix the bug here (stage 3)."""

# Tax is 10% (0.1).
TAX = 0.01


def total(prices):
    return round(sum(prices) * (1 + TAX))
