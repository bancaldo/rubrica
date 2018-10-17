#!/usr/bin/python
# delete.py
"""Delete Contact Frame for Rubrica App"""

import wx
from wx.lib.buttons import GenBitmapTextButton
from settings import IMG_PATH, FRAME_BG, BTN_BG


class DeleteFrame(wx.Frame):
    """Initial Core Frame"""
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.parent = parent
        self.panel = DeletePanel(parent=self)

        self.SetBackgroundColour(FRAME_BG)
        self.SetSize(325, 180)
        self.Centre()

        for widget in self.panel.GetChildren():
            if isinstance(widget, wx.Button):
                widget.Bind(wx.EVT_ENTER_WINDOW, self.parent.on_btn_enter)
                widget.Bind(wx.EVT_LEAVE_WINDOW, self.parent.on_btn_leave)

        self.Bind(wx.EVT_BUTTON, self.on_quit, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.panel.btn_delete)
        self.Bind(wx.EVT_COMBOBOX, self.on_contacts, self.panel.contacts)

        self.fill_contacts(self.parent.controller.get_contacts())

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
        self.parent = parent
        self.contacts = wx.ComboBox(self, -1, "", 
                                    choices=[], style=wx.CB_DROPDOWN)
        self.surname = wx.StaticText(self)
        self.name = wx.StaticText(self)
        self.btn_delete = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%strash.png" % IMG_PATH),
            'Delete'.rjust(20), size=(150, -1))

        self.btn_quit = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%sexit.png" % IMG_PATH),
            'Exit'.rjust(20), size=(150, -1))

        for button in (self.btn_delete, self.btn_quit):
            button.SetBezelWidth(1)
            button.SetBackgroundColour(BTN_BG)

        self.btn_delete.Disable()
        # Sizer
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
