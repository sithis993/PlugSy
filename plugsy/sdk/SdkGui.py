'''
PlugSy - SDK Gui - Helper GUI for creating, editing and deleting plugins
'''

# Import libs
# Add try here
import wx
from .SdkGuiAbs import PluginsHomeDirDialog
from .SdkGuiAbs import MainFrame
from ..Plugsy import Plugsy


class SdkGui(MainFrame):
    '''
    SDK Gui - Main
    '''

    def __init__(self):
        '''
        Constructor
        '''


        # Bind plugin events
        self.__set_events()

        MainFrame.__init__(self, parent=None)

        # Open Plugin home dir dialog
        self.__plugins_home_dir_dialog = _PluginsHomeDirDialog(parent=self)
        self.__plugins_home_dir_dialog.Show()


    def __set_events(self):
        '''
        Set GUI event handlers
        @return:
        '''

        pass




class _PluginsHomeDirDialog(PluginsHomeDirDialog):
    '''
    Child Plugins Directory Dialog
    '''

    def __init__(self, parent):
        '''
        Constructor
        @param parent: Parent Window. SDK MainFrame in this case
        '''
        self.__parent = parent

        # Disable Parent Window
        self.__parent.Disable()

        PluginsHomeDirDialog.__init__(self, parent=self.__parent)

