"""Cleans ticket IDs for Daiki's report.

Make clean() work. Read forum/q-1500.md for help.
Then run: python tickets.py
"""

# ---- Edit this part ----

def clean(ticket_id):
    """Remove 'ticket-' from the start of the ID. Keep the rest as it is."""
    raise NotImplementedError("Write this function. See forum/q-1500.md")


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
