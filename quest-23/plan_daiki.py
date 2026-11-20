"""Daiki's plan for the exporter. Run it to see what it writes. Do not edit."""
ORDERS = [("N0001", "salad", 2, "2026-12-11"), ("N0002", "sandwich", 1, "2026-12-11")]


def export(orders):
    lines = ["NOX 1.0"]
    for order_id, item, count, date in orders:
        lines.append(f"{order_id}|{item}|{count}|{date}")
    return "\n".join(lines)


print(export(ORDERS))
