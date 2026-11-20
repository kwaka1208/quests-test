# FAQ (phonebook 2.1)

## Moving from 1.x

phonebook 2.0 changed some names. Update your code like this:

| 1.x | 2.x |
| --- | --- |
| `phonebook.load(path)` | `phonebook.open_book(path)` |
| `book.search(name)` | `book.find(name)` |
| `person.note` | `person.note()` |

## I get `BookError: ... unknown format`. Why?

The book file may be old. Files made by phonebook 1.x use **format 1**,
but `open_book()` reads format 2 by default.
Open an old file with the `format` parameter. See the [API Reference](api.md).

You can see the format in the first line of the file.
A format 1 file starts with `PHONEBOOK 1`.

## My code prints `<bound method Person.note of ...>`. Why?

You forgot the `()`. In 2.x, `note` is a method. See [Moving from 1.x](#moving-from-1x).

## Who is in a book?

Use `book.names()`.
