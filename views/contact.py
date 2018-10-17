#!/usr/bin/python
# contact.py
"""Contact Frame for Rubrica App
This frame is used as Add Contact
Frame, and Edit Contact Frame
"""

import wx
from wx.lib.buttons import GenBitmapTextButton
from settings import IMG_PATH, FRAME_BG, BTN_BG


class ContactFrame(wx.Frame):
    """Initial Core Frame"""
    def __init__(self, parent, title, edit=False):
        self.edit = edit
        self.parent = parent
        super().__init__(parent=parent, title=title)
        self.panel = ContactPanel(parent=self)

        self.SetBackgroundColour(FRAME_BG)
        on_enter_callback = self.parent.parent.on_btn_enter if self.edit \
            else self.parent.on_btn_enter
        on_leave_callback = self.parent.parent.on_btn_leave if self.edit \
            else self.parent.on_btn_leave
        for widget in self.panel.GetChildren():
            if isinstance(widget, GenBitmapTextButton):
                widget.Bind(wx.EVT_ENTER_WINDOW, on_enter_callback)
                widget.Bind(wx.EVT_LEAVE_WINDOW, on_leave_callback)

        self.Bind(wx.EVT_BUTTON, self.on_quit, id=self.panel.btn_quit.GetId())
        self.Bind(wx.EVT_BUTTON, self.on_save, self.panel.btn_save)
        self.Bind(wx.EVT_TEXT, self.on_text_entry)

        self.SetSize(400, 300)
        self.Centre()

    # noinspection PyUnusedLocal
    def on_quit(self, event):
        self.parent.Enable()
        self.Destroy()

    # noinspection PyUnusedLocal
    def on_text_entry(self, event):
        """Enable the Save-button of add-contact-frame"""
        surname = self.panel.surname.GetValue()
        name = self.panel.name.GetValue()
        mobile = self.panel.mobile.GetValue()
        # Todo: VALIDATION
        if surname and name and mobile:
            self.panel.btn_save.Enable()

    # noinspection PyUnusedLocal
    def on_save(self, evt):
        """Button-Save on_click event handler of Add-contact frame"""
        surname = self.panel.surname.GetValue()
        name = self.panel.name.GetValue()
        address = self.panel.address.GetValue()
        mail = self.panel.mail.GetValue()
        phone = self.panel.phone.GetValue()
        mobile = self.panel.mobile.GetValue()
        if self.edit:  # child of child window!
            contact = self.parent.parent.controller.get_contact(surname, name)
        else:
            contact = self.parent.controller.get_contact(surname, name)

        if self.edit:  # here we are in edit-mode from find contact frame
            self.parent.parent.controller.update_contact(surname, name, address,
                                                         mail, phone, mobile)
            message = "Contact <%s %s> updated!" % (surname, name)
            self.show_message(message)
            self.parent.refresh_list_ctrl()  # refresh the parent-frame
        else:
            if contact:
                self.show_message("Contact %s %s already exists"
                                  % (surname, name))
            else:
                self.parent.controller.save_contact(surname, name, address,
                                                    mail, phone, mobile)
                message = "New contact <%s %s> saved!" % (surname, name)
                self.show_message(message)
            for widget in self.panel.GetChildren():
                if isinstance(widget, wx.TextCtrl):
                    widget.SetValue("")
            self.panel.btn_save.Disable()

    @staticmethod
    def show_message(message):
        wx.MessageBox(message, 'core info', wx.OK | wx.ICON_EXCLAMATION)


class ContactPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent

        self.surname = wx.TextCtrl(self, style=wx.ALIGN_LEFT)
        self.name = wx.TextCtrl(self, style=wx.ALIGN_LEFT)
        self.address = wx.TextCtrl(self, style=wx.ALIGN_LEFT)
        self.mail = wx.TextCtrl(self, style=wx.ALIGN_LEFT)
        self.phone = wx.TextCtrl(self, style=wx.ALIGN_LEFT)
        self.mobile = wx.TextCtrl(self, style=wx.ALIGN_LEFT)
        
        self.btn_save = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%ssave.png" % IMG_PATH),
            'Save'.rjust(20), size=(200, 45))

        self.btn_quit = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%sexit.png" % IMG_PATH),
            'Exit'.rjust(20), size=(200, 45))

        for button in (self.btn_save, self.btn_quit):
            button.SetBezelWidth(1)
            button.SetBackgroundColour(BTN_BG)

        self.btn_save.Disable()
        # sizer
        sizer = wx.FlexGridSizer(rows=7, cols=2, hgap=5, vgap=1)
        sizer.Add(wx.StaticText(self, -1, 'Surname*', style=wx.ALIGN_LEFT))
        sizer.Add(self.surname, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(wx.StaticText(self, -1, 'Name*', style=wx.ALIGN_LEFT))
        sizer.Add(self.name, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(wx.StaticText(self, -1, 'Address', style=wx.ALIGN_LEFT))
        sizer.Add(self.address, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(wx.StaticText(self, -1, 'Mail', style=wx.ALIGN_LEFT))
        sizer.Add(self.mail, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(wx.StaticText(self, -1, 'Phone', style=wx.ALIGN_LEFT))
        sizer.Add(self.phone, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(wx.StaticText(self, -1, 'Mobile*', style=wx.ALIGN_LEFT))
        sizer.Add(self.mobile, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(self.btn_save, 0, wx.EXPAND | wx.ALL, 1)
        sizer.Add(self.btn_quit, 0, wx.EXPAND | wx.ALL, 1)
        sizer.AddGrowableCol(1)
        self.SetSizer(sizer)
