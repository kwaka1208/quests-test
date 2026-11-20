# Your notes about the points fix

You wrote these notes during the v2.0 work. Use them for your devlog. Do not copy them as they are:
write full sentences, and tell the story.

- Issue #52 (Kaito): a 5-dollar lunch gave only 2 points. A 3-dollar lunch also gave 2 points.
- I asked on Northwind Answers. I learned that `round()` rounds 2.5 to 2. It rounds to the even number ("banker's rounding").
- Options I thought about:
  - keep `round()`: simple, but customers lose points. Not OK.
  - `Decimal` with ROUND_HALF_UP: correct, but heavy for one line.
  - `math.floor(price * 0.5 + 0.5)`: simple and correct for prices that are not negative. ← chosen
- PR #58. Misaki's review: one blocking comment. `refund_points()` gave points back instead of taking them. Fixed it.
- Released in v2.0.0. My GitHub ID is in the contributors. 🎉
- Next: move the points to cents, like the prices (PR #70, Haruto).
