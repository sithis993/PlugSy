'''
SDK GUI Launcher
'''

# Check os is Windows
import sys

try:
    import wx
except ImportError as ix:
    if not sys.platform.lower().startswith("win"):
        raise OSError("The PlugSy SDK GUI is currently only supported on Windows-based platforms.")
    else:
        raise ix

from plugsy.sdk.gui import SdkGui

def Go():
    app = wx.App()
    gui = SdkGui()
    gui.Show()
    app.MainLoop()

if __name__ == "__main__":
    Go()

