#!/usr/bin/python
# find.py

"""
Find Contact Frame for Rubrica App.
Double click on contact, enables the delete button and you can delete the
selected contact. Right click on contact, enables the edit frame that modifies
the contact values and stores the data to database.
"""

import os
import wx
from wx.lib.buttons import GenBitmapTextButton
from views.contact import ContactFrame


class FindFrame(wx.Frame):
    """Contact Manager Frame"""
    def __init__(self, parent, title):
        self.child = None
        self.parent = parent
        super().__init__(parent=parent, title=title)
        self.panel = FindPanel(parent=self)
        self.SetBackgroundColour('#FBFBEF')

        for widget in self.panel.GetChildren():
            if isinstance(widget, wx.Button):
                widget.Bind(wx.EVT_BUTTON, self.on_btn_chr)
                widget.Bind(wx.EVT_ENTER_WINDOW, self.on_btn_enter)
                widget.Bind(wx.EVT_LEAVE_WINDOW, self.on_btn_leave)

        for widget in self.panel.GetChildren():
            if isinstance(widget, GenBitmapTextButton):
                widget.Bind(wx.EVT_ENTER_WINDOW, self.on_btn_enter)
                widget.Bind(wx.EVT_LEAVE_WINDOW, self.on_btn_leave)

        self.Bind(wx.EVT_BUTTON, self.on_quit, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.panel.btn_delete)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_item_right_click, 
                  self.panel.list_ctrl)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_double_click, 
                  self.panel.list_ctrl)
        
        contacts = self.parent.controller.get_contacts_by_letter("A")
        self.fill_contacts(contacts)

        self.panel.list_ctrl.Focus(0)
        self.SetSize(700, 400)
        self.Centre()

    # noinspection PyUnusedLocal
    def on_quit(self, event):
        self.parent.Enable()
        self.Destroy()

    # noinspection PyUnusedLocal
    def on_btn_chr(self, event):
        """Chr-Button on_click event handler of Find-Contact frame """
        btn_chr = event.GetEventObject()
        char = btn_chr.GetLabel()
        self.parent.controller.set_mem_char(char)
        self.fill_contacts(self.parent.controller.get_contacts_by_letter(char))

    @staticmethod
    def on_btn_enter(event):
        """Into Button enter-mouse event handler"""
        obj = event.GetEventObject()
        obj.SetBackgroundColour('#F79F81')
        obj.Refresh()

    @staticmethod
    def on_btn_leave(event):
        """From Button leave-mouse event handler"""
        obj = event.GetEventObject()
        obj.SetBackgroundColour('#F8ECE0')
        obj.Refresh()

    # noinspection PyUnusedLocal
    def on_delete(self, event):
        """Button-Delete on_click event handler of Find-contact frame"""
        row = self.panel.list_ctrl.GetFocusedItem()
        surname = self.panel.list_ctrl.GetItem(row, 0).GetText()
        name = self.panel.list_ctrl.GetItem(row, 1).GetText()
        choice = wx.MessageBox('Deleting Contact %s %s...are you sure?'
                               % (surname, name), 'warning',
                               wx.YES_NO | wx.ICON_WARNING)
        if choice == wx.YES:
            self.parent.controller.delete_contact(surname, name)
            self.show_message("Contact %s %s deleted" % (surname, name))
            btn_chr = event.GetEventObject()
            char = btn_chr.GetLabel()
            self.fill_contacts(
                self.parent.controller.get_contacts_by_letter(char))
            self.panel.btn_delete.Disable()
            self.refresh_list_ctrl()

    # noinspection PyUnusedLocal
    def on_item_double_click(self, event):
        """Enable the delete-button of the find-frame"""
        self.panel.btn_delete.Enable()

    # noinspection PyUnusedLocal
    def on_item_right_click(self, event):
        """Edit all the selected contact data"""
        self.Disable()
        self.child = ContactFrame(parent=self, title='Edit Contact', edit=True)
        self.child.Show()
        # Fill Edit-contact frame with values of focused item
        row = self.panel.list_ctrl.GetFocusedItem()
        surname = self.panel.list_ctrl.GetItem(row, 0).GetText()
        name = self.panel.list_ctrl.GetItem(row, 1).GetText()
        address = self.panel.list_ctrl.GetItem(row, 2).GetText()
        mail = self.panel.list_ctrl.GetItem(row, 3).GetText()
        phone = self.panel.list_ctrl.GetItem(row, 4).GetText()
        mobile = self.panel.list_ctrl.GetItem(row, 5).GetText()

        self.child.panel.surname.SetValue(surname)
        self.child.panel.name.SetValue(name)
        self.child.panel.address.SetValue(address)
        self.child.panel.mail.SetValue(mail)
        self.child.panel.phone.SetValue(phone)
        self.child.panel.mobile.SetValue(mobile)

    def refresh_list_ctrl(self):
        char = self.parent.controller.get_mem_char()
        self.fill_contacts(
            self.parent.controller.get_contacts_by_letter(char))
        self.panel.btn_delete.Disable()

    def fill_contacts(self, contacts):
        """Fill the find-frame list-control with elements sorted by letter"""
        self.panel.list_ctrl.DeleteAllItems()
        for index, contact in enumerate(contacts):
            row = self.panel.list_ctrl.InsertItem(index, contact[0])
            self.panel.list_ctrl.SetItem(row, 1, contact[1])
            self.panel.list_ctrl.SetItem(row, 2, contact[2])
            self.panel.list_ctrl.SetItem(row, 3, contact[3])
            self.panel.list_ctrl.SetItem(row, 4, contact[4])
            self.panel.list_ctrl.SetItem(row, 5, contact[5])

    @staticmethod
    def show_message(message):
        wx.MessageBox(message, 'core info', wx.OK | wx.ICON_EXCLAMATION)


class FindPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        img_path = os.getcwd() + "\\images\\"
        self.parent = parent
        letters = [chr(i).upper() for i in range(ord('a'), ord('z')+1)]
        self.pos = 5
        for letter in letters:
            button = wx.Button(self, wx.ID_ANY, letter, (self.pos, 3), (26, 30))
            button.SetBackgroundColour('#F8ECE0')
            self.pos += 26

        wx.StaticLine(self, wx.ID_ANY, (0, 35), (700, 3))

        self.list_ctrl = wx.ListCtrl(self, wx.ID_ANY, (0, 50), (690, 200),
                                     wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.list_ctrl.InsertColumn(0, "Surname", wx.LIST_FORMAT_LEFT, 100)
        self.list_ctrl.InsertColumn(1, "Name", wx.LIST_FORMAT_LEFT, 100)
        self.list_ctrl.InsertColumn(2, "Address", wx.LIST_FORMAT_LEFT, 150)
        self.list_ctrl.InsertColumn(3, "mail", wx.LIST_FORMAT_LEFT, 150)
        self.list_ctrl.InsertColumn(4, "phone", wx.LIST_FORMAT_LEFT, 100)
        self.list_ctrl.InsertColumn(5, "mobile", wx.LIST_FORMAT_LEFT, 100)

        wx.StaticLine(self, wx.ID_ANY, (0, 270), (700, 3))

        self.btn_delete = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%strash.png" % img_path),
            'Delete'.rjust(20), (10, 300), (340, -1))
        self.btn_delete.SetBezelWidth(1)
        self.btn_delete.SetBackgroundColour('#F8ECE0')
        self.btn_delete.Disable()
        
        self.btn_quit = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%scancel.png" % img_path),
            'Cancel'.rjust(20), (345, 300), (340, -1))
        self.btn_quit .SetBezelWidth(1)
        self.btn_quit .SetBackgroundColour('#F8ECE0')
