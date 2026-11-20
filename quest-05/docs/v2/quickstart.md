# Quickstart (phonebook 2.1)

Open a book, find a person, and read the note:

```python
import phonebook

book = phonebook.open_book("staff.book")
person = book.find("Yui")
print(person.note())
```

Are you moving from phonebook 1.x? Read [Moving from 1.x](faq.md#moving-from-1x) first.

See the [API Reference](api.md) for more.
