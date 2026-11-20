# Devlog: Why we keep prices in cents

**Author:** @haruto-cto · **Date:** 2026-12-03

**TL;DR:** In v2.0, every price is a whole number of **cents**, like `500` for 5 dollars.
We chose cents because they never make rounding errors, and they are simple for everyone on the team.

## The problem

In v1, prices were numbers like `1.1`. One day, a customer bought two items for 1.1 and 2.2 dollars,
and the receipt said `3.3000000000000003`. Try it yourself:

    python -c "print(1.1 + 2.2)"

Computers keep these numbers in binary, and many decimal numbers cannot be kept exactly.
So small errors appear, and they grow when you add many prices.

## The options

We looked at three options.

1. **`float`** (like `1.1`): This is what we had. It is easy to write, but it makes rounding errors.
   For money, even one cent of error is not OK. So we did not choose it.
2. **`Decimal`** (from the `decimal` module): It has no rounding errors. But everyone must remember to use it
   everywhere, and one `float` in the wrong place breaks everything. It is also slower. We did not choose it, either.
3. **Cents as `int`** (like `110`): Whole numbers have no rounding errors, and they are fast and simple.
   The only cost is that we must divide by 100 when we show a price.

## The decision

We chose option 3: **cents as `int`**. It is a trade-off: we write a little more code to show prices,
but we never worry about rounding errors again.

## What's next

- Show prices as `1.10` dollars on the screen, with one helper function.
- Move the points to cents, too (see PR #70).
