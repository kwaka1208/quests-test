# Quickstart (phonebook 1.4)

> **Note:** This is the documentation for phonebook **1.4**.
> For the latest version, see [the 2.x documentation](../v2/quickstart.md).

Open a book, find a person, and read the note:

```python
import phonebook

book = phonebook.load("staff.book")
person = book.search("Yui")
print(person.note)
```

See the [API Reference](api.md) for more.
