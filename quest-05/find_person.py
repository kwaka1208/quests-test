# Daiki wrote this script many years ago, for phonebook 1.4.
# It finds a person in the book, and prints the person's note.
import phonebook

book = phonebook.load("staff.book")
person = book.search("Yui")
print(person.name, "says:", person.note)
