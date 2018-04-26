'''
SDK GUI Launcher
'''

from plugsy.sdk.gui import SdkGui

import wx
app = wx.App()
gui = SdkGui()
gui.Show()
app.MainLoop()

