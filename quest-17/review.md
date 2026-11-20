# Pull Request #58: fix: round half up when giving points

**Author:** you · **Branch:** `fix-points` → `main`

Closes #52

---

## Review by @daiki-ops · 💬 Commented

> LGTM! Nice to see the points mystery solved. 🎉
> I did not read the tests yet, so I'm only leaving a comment for now. Misaki will do the full review.

---

## Review by @kaito-m · ✅ Approved

> I tested it with 3, 5 and 7 dollars. Works for me.

**`points.py`, line 19** — `describe()`

> **nit:** "1 points" sounds a little strange in English. Maybe "1 point" when it is one?
> Not a big deal. Feel free to merge without it.

---

## Review by @misaki-w · ❌ Changes requested

> Thank you! The rounding fix is great. I have a few comments.
> One of them must be fixed before we merge. The others are up to you.

**`points.py`, line 10** — `points()`

> **optional:** You could use the `decimal` module for money. It is fine as it is for now.

**`points.py`, line 15** — `refund_points()`

> **blocking:** When a customer returns a lunch, we must **take back** the points.
> Right now `refund_points()` returns a positive number, so the customer gets points **again**!
> It should return a negative number: `refund_points(5)` should be `-3`.

**`points.py`, line 18** — `describe()`

> **question:** Why is the price in dollars here? The new `prices.py` for v2.0 uses cents.
> Just curious. No change needed. You can answer in a reply.

**`points.py`, line 23** — `main()`

> **nit:** Maybe add 1 dollar to the list of prices? Not needed for this pull request.
