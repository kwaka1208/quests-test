# Northwind Order Export (NOX) 1.0

**Author:** @haruto-cto · **Status:** Draft for v3

This spec describes the file that Northwind Lunch v3 uses to export orders.
Other apps (like the kitchen system) read this file, so every writer must follow it.

## Keywords

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** in this document
are to be read as described in RFC 2119.

## Rules

1. The first line of the file MUST be `NOX 1.0`.
2. Each order MUST be on one line, in this form: `ID|ITEM|COUNT|DATE`.
3. `ID` MUST be the letter `N` and four digits, like `N0042`.
4. `COUNT` MUST be a whole number from 1 to 20.
5. `DATE` MUST be in the form `YYYY-MM-DD`.
6. `ITEM` SHOULD be written in small letters, like `salad`.
7. The last line of the file SHOULD be `END`.
8. A line that starts with `#` is a comment. Writers MAY add comments.
9. The file MUST NOT contain prices. (Prices change every month. The kitchen reads them from the menu.)
10. Each `ID` MUST be different in the file.
11. Readers MUST ignore comment lines.

## Example

```
NOX 1.0
# orders for Friday
N0001|salad|2|2026-12-11
N0002|sandwich|1|2026-12-11
END
```
