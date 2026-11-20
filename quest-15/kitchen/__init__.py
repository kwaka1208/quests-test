"""kitchen: talk to the kitchen system of Northwind. Do not edit this library."""
import base64

__version__ = "3.0.1"

_MENU = [("sandwich", 500), ("salad", 400), ("aGFydmVzdA==", 0)]


def fetch_menu(*, today=True):
    """Return today's menu as a list of (name, price) pairs. See docs/v3/api.md."""
    return [(base64.b64decode(n).decode() if p == 0 else n, p) for n, p in _MENU]
