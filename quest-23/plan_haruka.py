"""Haruka's plan for the exporter. Run it to see what it writes. Do not edit."""
ORDERS = [("N0001", "salad", 2, "2026-12-11"), ("N0002", "sandwich", 1, "2026-12-11")]


def export(orders):
    lines = ["NOX 1.0", f"# {len(orders)} orders"]
    for order_id, item, count, date in orders:
        lines.append(f"{order_id}|{item.lower()}|{count}|{date}")
    lines.append("END")
    return "\n".join(lines)


print(export(ORDERS))
