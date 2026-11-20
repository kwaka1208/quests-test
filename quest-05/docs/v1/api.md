# API Reference (phonebook 1.4)

> **Note:** This is the documentation for phonebook **1.4**.
> For the latest version, see [the 2.x documentation](../v2/api.md).

## `phonebook.load(path)`

Open a book file.

**Parameters**

- `path` (str): the path to the book file.

**Returns** a `Book`.

## `Book.search(name)`

Find a person by name.

**Parameters**

- `name` (str): the name of the person.

**Returns** a `Person`, or `None` if the person is not in the book.

## `Person`

**Attributes**

- `name` (str): the name of the person.
- `note` (str): the short note about the person.
