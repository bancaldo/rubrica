#!/usr/bin/python
# delete.py
"""Delete Contact Frame for Rubrica App"""

import os
import wx
from wx.lib.buttons import GenBitmapTextButton


class DeleteFrame(wx.Frame):
    """Initial Core Frame"""
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.parent = parent
        self.panel = DeletePanel(parent=self)

        self.SetBackgroundColour('#FBFBEF')
        self.SetSize(325, 180)
        self.Centre()

        self.fill_contacts(self.parent.controller.get_contacts())

        self.panel.btn_delete.Bind(wx.EVT_ENTER_WINDOW, self.on_btn_enter)
        self.panel.btn_delete.Bind(wx.EVT_LEAVE_WINDOW, self.on_btn_leave)
        self.panel.btn_quit.Bind(wx.EVT_ENTER_WINDOW, self.on_btn_enter)
        self.panel.btn_quit.Bind(wx.EVT_LEAVE_WINDOW, self.on_btn_leave)
        self.Bind(wx.EVT_BUTTON, self.on_quit, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.panel.btn_delete)
        self.Bind(wx.EVT_COMBOBOX, self.on_contacts, self.panel.contacts)

    # noinspection PyUnusedLocal
    def on_quit(self, event):
        self.parent.Enable()
        self.Destroy()

    # noinspection PyUnusedLocal
    def on_contacts(self, event):
        contact_string = self.panel.contacts.GetStringSelection()
        surname, name = self.parent.controller.split_name(contact_string)
        self.panel.surname.SetLabel(surname)
        self.panel.name.SetLabel(name)
        self.panel.btn_delete.Enable()

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

    def fill_contacts(self, iterable):
        self.panel.contacts.Clear()
        self.panel.contacts.AppendItems(iterable)

    # noinspection PyUnusedLocal
    def on_delete(self, evt):
        """Button-Delete on_click event handler of Del-Contact"""
        contact_string = self.panel.contacts.GetStringSelection()
        surname, name = self.parent.controller.split_name(contact_string)
        choice = wx.MessageBox('Deleting Contact %s %s...are you sure?'
                               % (surname, name), 'warning',
                               wx.YES_NO | wx.ICON_WARNING)
        if choice == wx.YES:
            self.parent.controller.delete_contact(surname, name)
            self.show_message("Contact %s %s deleted" % (surname, name))
            self.fill_contacts(self.parent.controller.get_contacts())
            self.panel.surname.SetLabel("")
            self.panel.name.SetLabel("")
            self.panel.btn_delete.Disable()

    @staticmethod
    def show_message(message):
        wx.MessageBox(message, 'core info', wx.OK | wx.ICON_EXCLAMATION)


class DeletePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        img_path = os.getcwd() + "\\images\\"
        self.parent = parent
        self.contacts = wx.ComboBox(self, -1, "", 
                                    choices=[], style=wx.CB_DROPDOWN)
        self.surname = wx.StaticText(self)
        self.name = wx.StaticText(self)
        self.btn_delete = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%strash.png" % img_path),
            'Delete'.rjust(20), size=(150, -1))
        self.btn_delete.SetBezelWidth(1)
        self.btn_delete.SetBackgroundColour('#F8ECE0')
        self.btn_delete.Disable()
        
        self.btn_quit = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%scancel.png" % img_path),
            'Cancel'.rjust(20), size=(150, -1))
        self.btn_quit.SetBezelWidth(1)
        self.btn_quit.SetBackgroundColour('#F8ECE0')
        
        sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=1)
        sizer.Add(wx.StaticText(self, -1, 'Surname', style=wx.ALIGN_LEFT))
        sizer.Add(self.surname, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(wx.StaticText(self, -1, 'Name', style=wx.ALIGN_LEFT))
        sizer.Add(self.name, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(self.btn_delete, 0, wx.EXPAND | wx.ALL, 1)
        sizer.Add(self.btn_quit, 0, wx.EXPAND | wx.ALL, 1)
        sizer.AddGrowableCol(1)
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        outer_sizer.Add(self.contacts, 0, wx.EXPAND | wx.ALL, 5)
        outer_sizer.Add(sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(outer_sizer)
