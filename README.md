# Rubrica 3.0

Rubrica 3.0 is a simple App written in python 3, which creates a contacts agenda.
This is simply an exercise to use database and graphic library.

python modules used:
- wxPython for Graphics
- sqlalchemy for database and ORM

## How to Install

If you use a virtualenv install requirements via pip:

```
pip install -r requirements.txt
```

In the settings.py file it is possible to set the database file name,
the images path and the widget background colors.

Simply run the main.py file to create database and start the app

## How to use

The GUI is a core frame with five buttons:
### Info

open a mini frame with some informations about this simple app

### Add contact

open a child frame to insert the new contact data to save on database

### Delete contact

open a child frame to delete contact from database

### Find contact

open a child frame to find contacts by letter.
Here it's possible to delete a contact by double-clicking on name or
edit contact data simply by right-clicking on it.

### Exit

...

## Todo
Validators during new contact saving.

## License

GPL
