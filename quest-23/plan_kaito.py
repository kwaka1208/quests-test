"""Kaito's plan for the exporter. Run it to see what it writes. Do not edit."""
PRICES = {"salad": 400, "sandwich": 500}
ORDERS = [("N0001", "salad", 2, "2026-12-11"), ("N0002", "sandwich", 1, "2026-12-11")]


def export(orders):
    lines = ["NOX 1.0", "# with prices, so the kitchen can check the total"]
    for order_id, item, count, date in orders:
        lines.append(f"{order_id}|{item}|{count}|{date}|{PRICES[item]}")
    lines.append("END")
    return "\n".join(lines)


print(export(ORDERS))
