"""Lunch points of Northwind. This is the code in your pull request #58.

Fix only what the reviewers say you MUST fix before the merge.
"""
import math


def points(price):
    # Round half up: 2.5 gives 3.
    return math.floor(price * 0.5 + 0.5)


def refund_points(price):
    # When a customer returns a lunch, we take back the points.
    return points(price)


def describe(price):
    return f"A {price}-dollar lunch gives {points(price)} points."


def main():
    for price in (3, 5, 7):
        print(describe(price))


if __name__ == "__main__":
    main()
