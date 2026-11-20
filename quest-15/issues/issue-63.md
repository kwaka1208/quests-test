# Issue #63: Total price is wrong on the beta server

**Labels:** `bug`, `confirmed` · **State:** open

---

**@tomoki-s** commented

A sandwich and a coffee should cost 770 cents with tax. The beta server says 707.

**Steps to reproduce:**

1. Run `python total.py`.

---

**@kaito-m** commented

I can reproduce it. It started after PR #61 was merged. Before that, the total was right.

---

**@haruto-cto** (maintainer) commented

Thanks. PR #61 changed the tax. Please look at its diff (`pr-61.diff`) and fix `prices.py`.
