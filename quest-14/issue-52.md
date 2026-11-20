# Issue #52: A 5-dollar lunch gives only 2 points

**Labels:** `bug` · **Opened by:** @kaito-m

A 3-dollar lunch gives 2 points, and a 5-dollar lunch **also** gives 2 points.
Customers get half of the price as points, so a 5-dollar lunch should give 3 points (2.5, rounded up).

**Steps to reproduce:**

1. Run `python points.py`.

**Expected:** `A 5-dollar lunch gives 3 points.`

**Actual:** `A 5-dollar lunch gives 2 points.`

---

**@misaki-w**: Good catch! Python's `round()` rounds 2.5 to 2 (to the even number). Let's round half up instead.
Can our new teammate take this one?
