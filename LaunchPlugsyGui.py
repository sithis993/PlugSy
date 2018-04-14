'''
SDK TEST
@todo: Add character checking to make sure the name doesn't contain bad chars
@todo: Add dependency writing and other fields
'''

from plugsy.sdk.SdkGui import SdkGui

import wx
app = wx.App()
gui = SdkGui()
gui.Show()
app.MainLoop()

