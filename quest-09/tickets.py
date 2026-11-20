"""Cleans ticket IDs for Daiki's report.

Make clean() work. Then run: python tickets.py

Note from Daiki: I asked about this on Northwind Answers before:
https://kwaka1208.github.io/northwind-developers/answers/q-1500.html
(the same page is in forum/q-1500.md)
"""

# ---- Edit this part ----

def clean(ticket_id):
    """Remove 'ticket-' from the start of the ID. Keep the rest as it is."""
    raise NotImplementedError("Write this function.")


# ---- Do not edit below this line ----
import base64
import sys


def main():
    cases = [("ticket-42", "42"), ("ticket-kettle", "kettle"), ("notes-7", "notes-7")]
    for given, expected in cases:
        result = clean(given)
        if result != expected:
            print(f"clean({given!r}) が {result!r} を返しました。正しくは {expected!r} です。")
            print("まだです。回答とコメントをもう一度読みましょう。")
            return 1
    print("すべてのチェックに合格しました！")
    print("答えになる単語:", base64.b64decode("cHJpc20=").decode())
    return 0


if __name__ == "__main__":
    sys.exit(main())
