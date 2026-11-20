"""phonebook: read the phone books of Northwind.

Do not edit this library. Read its documentation in the docs folder.
"""
import base64
import json
from pathlib import Path

__version__ = "2.1.0"
__all__ = ["BookError", "Book", "Person", "open_book"]

_FORMAT1_HEADER = "PHONEBOOK 1"


class BookError(Exception):
    """A book cannot be read, or a person is not in it."""


class Person:
    def __init__(self, name, secret):
        self.name = name
        self._secret = secret

    def note(self):
        """Return the short note about this person."""
        return base64.b64decode(self._secret).decode()

    def __repr__(self):
        return f"Person({self.name!r})"


class Book:
    def __init__(self, path, people):
        self.path = path
        self._people = people

    def names(self):
        """Return the names of all people in the book."""
        return sorted(self._people)

    def find(self, name):
        """Return the person called name. Upper and lower case do not matter."""
        for key, secret in self._people.items():
            if key.lower() == name.strip().lower():
                return Person(key, secret)
        raise BookError(f"there is no person called {name!r} in {self.path}")


def _read_format1(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FORMAT1_HEADER:
        return None
    people = {}
    for line in lines[1:]:
        if "|" in line:
            name, secret = line.split("|", 1)
            people[name.strip()] = secret.strip()
    return people


def _read_format2(text):
    try:
        data = json.loads(text)
    except ValueError:
        return None
    if not isinstance(data, dict) or data.get("format") != 2:
        return None
    return dict(data.get("people", {}))


def open_book(path, *, format=2):
    """Open a book file, and return a Book. See docs/v2/api.md."""
    readers = {1: _read_format1, 2: _read_format2}
    if format not in readers:
        raise BookError(f"format must be 1 or 2, not {format!r}")
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise BookError(f"cannot find the book file {path!r}") from None
    people = readers[format](text)
    if people is None:
        raise BookError(f"cannot read {path!r}: unknown format (expected format {format})")
    return Book(str(path), people)
