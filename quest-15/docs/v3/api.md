# API Reference (kitchen 3.0)

## `kitchen.fetch_menu(*, today=True)`

**Returns** the menu as a **list** of `(name, price)` pairs.

- `today` (bool, optional, keyword-only): `True` for today's menu. Default: `True`.

*Changed in version 3.0: renamed from `get_menu()`. It returns a list of pairs, not a dict.*

## Removed

- `kitchen.get_menu()`: *Removed in version 3.0.* Use `fetch_menu()`.
