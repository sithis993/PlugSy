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

if __name__ == "__main__":
    Go()

