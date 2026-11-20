# API Reference (phonebook 2.1)

## `phonebook.open_book(path, *, format=2)`

Open a book file.

**Parameters**

- `path` (str): the path to the book file.
- `format` (int, optional): the format version of the file. Default: `2`.
  Use `1` for files made by phonebook 1.x.
  This is a keyword-only argument: write `format=1`, not just `1`.

**Returns** a `Book`.

**Raises** `BookError` if the file is not found, or if it is not in the given format.

*Added in version 2.0.*
*Changed in version 2.1: added the `format` parameter. Before 2.1, only format 2 files could be opened.*

## `Book.find(name)`

Find a person by name. Upper and lower case do not matter.

**Parameters**

- `name` (str): the name of the person.

**Returns** a `Person`.

**Raises** `BookError` if the person is not in the book.

*Changed in version 2.0: renamed from `search()`. It raises `BookError` instead of returning `None`.*

## `Book.names()`

**Returns** a list of the names of all people in the book.

*Added in version 2.0.*

## `Person`

**Attributes**

- `name` (str): the name of the person.

**Methods**

- `note()`: returns the short note about the person (str).

*Changed in version 2.0: `note` is now a method. In 1.x, it was an attribute.
Write `person.note()`, not `person.note`.*

## `BookError`

The exception that phonebook raises when something goes wrong.

## Removed

- `phonebook.load(path)`: *Removed in version 2.0.* Use `open_book()`.
