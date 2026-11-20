"""A helper for Kaito's test tool.

Make is_mapping() work. Then run: python mapping.py

Note from Kaito: I asked about this on Northwind Answers once.
This page helped me:
https://kwaka1208.github.io/northwind-developers/answers/q-1042.html
(the same page is in forum/q-1042.md)
"""

# ---- Edit this part ----

def is_mapping(value):
    """Return True if value works like a dictionary, and False if not."""
    raise NotImplementedError("Write this function.")


# ---- Do not edit below this line ----
import base64
import sys
from collections import OrderedDict, UserDict


class Box:
    """Not a dictionary. It only has a keys() method."""

    def keys(self):
        return []


def main():
    cases = [({}, "{}", True), (OrderedDict(), "OrderedDict()", True), (UserDict(), "UserDict()", True),
             ([], "[]", False), ("abc", "'abc'", False), (Box(), "Box()", False)]
    for value, shown, expected in cases:
        result = is_mapping(value)
        if result is not expected:
            print(f"is_mapping({shown}) が {result!r} を返しました。正しくは {expected} です。")
            print("まだです。回答とコメントをもう一度読みましょう。")
            return 1
    print("すべてのチェックに合格しました！")
    print("答えになる単語:", base64.b64decode("YmVhY29u").decode())
    return 0


if __name__ == "__main__":
    sys.exit(main())
