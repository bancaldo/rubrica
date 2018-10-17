#!/usr/bin/python
# info.py
"""Info Frame for About choice"""

import wx
import wx.html
from wx.lib.buttons import GenBitmapTextButton
from settings import IMG_PATH, BTN_BG


class InfoFrame(wx.Frame):
    """Frame for Info text"""
    def __init__(self, parent, title):
        self.parent = parent
        super().__init__(parent=parent, title=title)
        self.panel = InfoPanel(parent=self)

        self.Bind(wx.EVT_BUTTON, self.on_quit, id=self.panel.btn_quit.GetId())
        self.panel.btn_quit.Bind(wx.EVT_ENTER_WINDOW, self.parent.on_btn_enter)
        self.panel.btn_quit.Bind(wx.EVT_LEAVE_WINDOW, self.parent.on_btn_leave)

        self.SetSize(400, 400)
        self.SetBackgroundColour(BTN_BG)
        self.Centre()

    # noinspection PyUnusedLocal
    def on_quit(self, event):
        self.parent.Enable()
        self.Destroy()


class InfoPanel(wx.Panel):
    """Panel containing html text"""
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        text = """
        <html><body bgcolor="#F78181"><center>
        <table bgcolor="#FBFBEF" width="100%" cellspacing="0" cellpadding="0"
         border="1">
        <tr><td align="center"><h1>Rubrica v3.0</h1></td></tr></table></center>
        <p><b>Rubrica</b> is a simple phone-book realized with:<br>
        <b>- wxPython 4.0</b> for Graphics<br>
        <b>- Sqlite</b> for database structure<br>
        <b>- SQLAlchemy</b> for Object Relation Mapping<br>
        I've tried to use a Model-View-Controller pattern-like.<br>
        web-site: <b>www.bancaldo.wordpress.com</b><br>
        last revision: may 17, 2015</p></body></html>
        """
        html = wx.html.HtmlWindow(self)
        html.SetPage(text)
        self.btn_quit = GenBitmapTextButton(
            self, wx.ID_ANY, wx.Bitmap("%sexit.png" % IMG_PATH),
            'Exit'.rjust(20), (350, 150))
        self.btn_quit.SetBezelWidth(1)
        self.btn_quit.SetBackgroundColour(BTN_BG)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_quit, 0, wx.ALIGN_CENTER | wx.EXPAND, 5)
        self.SetSizer(sizer)
