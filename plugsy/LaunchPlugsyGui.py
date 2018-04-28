'''
SDK GUI Launcher
'''

from plugsy.sdk.gui import SdkGui
import wx

def Go():
    app = wx.App()
    gui = SdkGui()
    gui.Show()
    app.MainLoop()

