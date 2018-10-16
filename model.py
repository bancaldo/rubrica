#!/usr/bin/python
# model.py

"""Data module for sql alchemy ORM"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class Model:
    """Model class with common application data"""
    base = declarative_base()
    engine = create_engine('sqlite:///contacts.db', echo=True)
    metadata = base.metadata
    metadata.create_all(engine)
    m_session = sessionmaker(bind=engine)
    session = m_session()

    def __init__(self):
        self.char = "A"
        self.contact = None
        self.init_database()

    def init_database(self):
        self.metadata.create_all(self.engine)

    def get_mem_contact(self):
        """return the in-memory object -> Contact"""
        print("INFO: getting in-memory object...")
        return self.contact

    def set_mem_contact(self, contact_object):
        """Set the in-memory object"""
        print("INFO: setting in-memory object...")
        self.contact = contact_object

    def get_mem_char(self):
        """return the in-memory char -> char"""
        print("INFO: getting in-memory char...")
        return self.char

    def set_mem_char(self, char):
        """Set the in-memory char"""
        print("INFO: setting in-memory char...")
        self.char = char

    def get_contact(self, surname, name):
        """
        Get contact by surname and name -> Contact object
        Get contact by surname and name
        """
        result = self.session.query(Contact).filter_by(
            surname=surname.upper(), name=name.capitalize()).first()
        return result

    def get_contacts(self):
        """Get all contacts -> iterable"""
        return self.session.query(Contact).all()

    def get_contacts_by_letter(self, letter):
        """
        get_contacts_by_letter(letter) -> contact list
        Get the list of all contacts with Surname starting by letter
        """
        return self.session.query(Contact).filter(
            Contact.surname.like("%s%%" % letter)).all()

    def save_contact(self, surname, name, address, mail, phone, mobile):
        """
        save_contact(surname, name, address, mail, phone, mobile)
        Save contact on the database
        """
        contact = Contact(name=name.capitalize(), surname=surname.upper(),
                          address=address, mail=mail, phone=phone, 
                          mobile=mobile)
        self.session.add(contact)
        self.session.commit()
        print("INFO: contact %s %s stored on database!"
              % (surname.upper(), name.capitalize()))

    def update_contact(self, surname, name, address, mail, phone, mobile):
        """
        update_contact(surname, name, address, mail, phone, mobile)
        Update contact on the database
        """
        contact = self.get_contact(surname.upper(), name.capitalize())
        if not contact:
            contact = self.get_mem_contact()

        contact.surname = surname.upper()
        contact.name = name.capitalize()
        contact.address = address
        contact.mail = mail
        contact.phone = phone
        contact.mobile = mobile
        self.session.commit()
        print("INFO: contact %s %s updated!" % (surname.upper(),
                                                name.capitalize()))

    def delete_contact(self, surname, name):
        """
        delete_contact(surname, name)
        Delete contact by surname and name, from database
        """
        contact = self.get_contact(surname.upper(), name.capitalize())
        if contact:
            self.session.delete(contact)
            self.session.commit()
            print("INFO: contact %s %s deleted!" % (surname, name))
        else:
            print("ERROR: contact %s %s not found!" % (surname, name))


class Contact(Model.base):
    """Contact class for ORM Mapping"""
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    address = Column(String)
    mail = Column(String)
    mobile = Column(String)
    phone = Column(String)
    
    def __init__(self, name, surname, address, mail, mobile, phone):
        self.name = name
        self.surname = surname
        self.address = address
        self.mail = mail
        self.mobile = mobile
        self.phone = phone

    def __repr__(self):
        return "<Contact ('%s %s')>" % (self.surname, self.name)
