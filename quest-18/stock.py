"""Stock of the kitchen. This is the code in Daiki's pull request #66."""

STOCK = {"salad": 10, "sandwich": 8}


def take(item, n):
    # take n items from the stock
    if STOCK[item] > n:
        STOCK[item] -= n
        return True
    return False


def report():
    for k, v in STOCK.items():
        print(k + ": " + str(v))
