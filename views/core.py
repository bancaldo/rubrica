#!/usr/bin/python
# core.py
"""Core Frame for Rubrica App"""

import wx
import os
from wx.lib.buttons import GenBitmapTextButton

from views.contact import ContactFrame
from views.info import InfoFrame
from views.delete import DeleteFrame
from views.find import FindFrame


class CoreFrame(wx.Frame):
    """Initial Core Frame"""
    def __init__(self, parent, title, controller):
        self.child = None
        super().__init__(parent=parent, title=title)
        self.controller = controller
        self.panel = CorePanel(parent=self)
        self.SetBackgroundColour('#FBFBEF')
        # GENERIC BINDINGS
        for widget in self.panel.GetChildren():
            if isinstance(widget, GenBitmapTextButton):
                widget.Bind(wx.EVT_ENTER_WINDOW, self.on_btn_enter)
                widget.Bind(wx.EVT_LEAVE_WINDOW, self.on_btn_leave)

        # BINDINGS
        self.Bind(wx.EVT_BUTTON, self.on_quit, self.panel.btn_exit)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.panel.btn_add)
        self.Bind(wx.EVT_BUTTON, self.on_info, self.panel.btn_info)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.panel.btn_delete)
        self.Bind(wx.EVT_BUTTON, self.on_find, self.panel.btn_find)

        self.SetSize(300, 300)
        self.Centre()

    # noinspection PyUnusedLocal
    def on_quit(self, event):
        """Button Quit callback: Destroy the frame"""
        self.Destroy()

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
    def on_info(self, event):
        """Button-Info on_click event handler"""
        self.Disable()
        self.child = InfoFrame(parent=self, title='Info')
        self.child.Show()

    # noinspection PyUnusedLocal
    def on_add(self, event):
        """Button Add callback: Open the 'Add Contact' frame"""
        self.Disable()
        self.child = ContactFrame(parent=self, title='Save Contact')
        self.child.Show()

    # noinspection PyUnusedLocal
    def on_find(self, event):
        """Button-Find on_click event handler"""
        self.Disable()
        self.child = FindFrame(parent=self, title='Find Contact')
        self.child.Show()

    # noinspection PyUnusedLocal
    def on_delete(self, event):
        """Button-Delete on_click event handler"""
        self.Disable()
        self.child = DeleteFrame(parent=self, title='Delete Contact')
        self.child.Show()


class CorePanel(wx.Panel):
    def __init__(self, parent):
        super(CorePanel, self).__init__(parent=parent)
        img_path = os.getcwd() + "\\images\\"
        self.parent = parent
        self.btn_info = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%sinfo.png" % img_path),
            'About...'.rjust(15), size=(280, 45))

        self.btn_add = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%sadd.png" % img_path),
            'Add Contact'.rjust(15), size=(280, 45))
        
        self.btn_delete = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%sdelete.png" % img_path),
            'Delete Contact'.rjust(15), size=(280, 45))

        self.btn_find = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%ssearch.png" % img_path),
            'Find Contact'.rjust(15), size=(280, 45))

        self.btn_exit = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%sexit.png" % img_path),
            'Exit'.rjust(15), size=(280, 45))
        
        for widget in self.GetChildren():
            if isinstance(widget, GenBitmapTextButton):
                widget.SetBezelWidth(1)
                widget.SetBackgroundColour('#F8ECE0')

        # BUTTONS SIZER
        sizer = wx.FlexGridSizer(rows=5, cols=1, hgap=5, vgap=0)
        sizer.Add(self.btn_info, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(self.btn_add, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(self.btn_delete, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(self.btn_find, 0, wx.EXPAND | wx.ALL, 4)
        sizer.Add(self.btn_exit, 0, wx.EXPAND | wx.ALL, 4)
        sizer.AddGrowableCol(0)
        self.SetSizer(sizer)
