# Notes from the meeting: the points card file (v3)

The kitchen, the lunch app and the support desk will all read this file.
Haruto asked you to turn these notes into a spec.

Here is what the team decided:

- The file is JSON.
- `version` is always the number `1`.
- `card` is the card ID: the letter `C` and four digits, like `C0042`.
- `points` is the number of points now. It is a whole number, and it can never be negative.
- `history` is a list of changes. The oldest change comes first.
- Each change has a `date` (YYYY-MM-DD) and a `change` (a whole number; negative for refunds).
- A change can also have a `note`, like "refund", if you want. It is not required.
- **Never** put the customer's name in the file. (Privacy!)
- It is better to keep only the last 100 changes in `history`, so the file stays small. But older changes are not an error.

Two example files from the team are in `examples/`.
