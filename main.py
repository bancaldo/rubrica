#!/usr/bin/python
# main.py
"""Rubrica 3.0 by Bancaldo"""

import wx
from model import Model
from views.core import CoreFrame


class Controller:
    """Controller Object"""
    def __init__(self):
        """Constructor"""
        self.model = Model()
        self.core = CoreFrame(parent=None, title='Rubrica 3.0', controller=self)
        self.core.Show()

    def get_contacts(self):
        """
        get_contacts -> contact list
        Get the list of all contacts as Surname-Name form
        """
        contacts = ['%s %s' % (contact.surname, contact.name) 
                    for contact in self.model.get_contacts()]
        contacts.sort()
        return contacts

    def get_contact(self, surname, name):
        """
        get_contact(surname, name) -> contact object
        Return Contact by surname and name if exists
        """
        return self.model.get_contact(surname, name)

    def get_contacts_by_letter(self, letter):
        """
        get_contacts_by_letter(letter) -> contact list
        Get the list of all contacts with Surname starting by letter
        """
        contacts = [(contact.surname, contact.name, contact.address,
                     contact.mail, contact.phone, contact.mobile)
                    for contact in self.model.get_contacts_by_letter(letter)]
        # here I Sort the list of contacts by surname and name
        contacts.sort(key=lambda value: (value[0], value[1]))
        return contacts

    def update_contact(self, surname, name, address, mail, phone, mobile):
        """
        update_contact(surname, name, address, mail, phone, mobile)
        Update contact in database found by surname and name
        """
        self.model.update_contact(surname, name, address, mail, phone, mobile)

    def save_contact(self, surname, name, address, mail, phone, mobile):
        """
        save_contact(surname, name, address, mail, phone, mobile)
        Save new contact in database
        """
        self.model.save_contact(surname, name, address, mail, phone, mobile)

    @staticmethod
    def split_name(contact_string):
        """
        split_name(contact_string) -> surname, name
        split the string passed as argument in surname and name
        """
        values = contact_string.split(" ")
        name = values[-1]
        surname = " ".join(values[:-1])
        return surname.upper(), name.capitalize()

    def delete_contact(self, surname, name):
        """
        delete_contact(surname, name)
        Delete the contact from database which has surname and name args
        """
        self.model.delete_contact(surname, name)

    def get_mem_char(self):
        """
        get_mem_char()
        return the in-memory char -> char
        """
        return self.model.get_mem_char()

    def set_mem_char(self, char):
        """
        set_mem_char(char)
        Set the in-memory char to char
        """
        self.model.set_mem_char(char)


def run():
    """Application starter"""
    app = wx.App()
    Controller()
    app.MainLoop()


if __name__ == '__main__':
    run()
