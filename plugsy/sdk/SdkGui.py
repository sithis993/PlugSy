'''
PlugSy - SDK Gui - Helper GUI for creating, editing and deleting plugins
'''

# Import libs
import wx
import os
import re
import importlib
from .SdkGuiAbs import PluginsHomeDirDialog
from .SdkGuiAbs import MainFrame
from .SdkGuiAbs import NewPluginDialog
from .Sdk import Sdk
from .Exceptions import *
from ..Plugsy import Plugsy


class SdkGui(MainFrame):
    '''
    SDK Gui - Main
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__sdk = None
        self.__plugins_home_dir = None
        self.__loaded_plugins = {}
        self.__selected_plugin = None
        MainFrame.__init__(self, parent=None)

        # Bind plugin events
        self.__set_events()

        # Open Plugin home dir dialog
        self.__plugins_home_dir_dialog = _PluginsHomeDirDialog(parent=self)
        self.__plugins_home_dir_dialog.Show()


    def __set_events(self):
        '''
        Set GUI event handlers
        @return:
        '''

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.__set_selected_plugin, self.PluginsTreeCtrl)
        self.Bind(wx.EVT_MENU, self.__create_new_plugin, self.NewPluginMenuItem)


    def reload_plugins(self):
        '''
        Reloads plugins from specified plugins home directory
        @return:
        '''

        #self.__loaded_plugins = self.__sdk.get_plugins()
        #self.__populate_tree()
        self.set_plugins_home(self.__plugins_home_dir)


    def set_plugins_home(self, plugins_home_dir):
        '''
        Sets the plugins home dir to the specified directory and loads contained plugins
        @param plugins_home_dir: Absolute path to the plugins home
        @return:
        '''
        self.__plugins_home_dir = plugins_home_dir

        # Init SDK and load plugins
        self.__sdk = Sdk(plugins_home_dir)
        self.__loaded_plugins = self.__sdk.get_plugins()

        # Add plugins to GUI
        self.__populate_tree()

        # Set status bar
        self.__set_status_bar_message("Plugins Home - %s" % plugins_home_dir)


    def __populate_tree(self):
        '''
        Populates the tree ctrl with loaded plugins
        @return:
        '''

        # Clear tree. Might not be the most efficient approach... Should only add new item
        self.PluginsTreeCtrl.DeleteAllItems()

        #raise Exception(self.PluginsTreeCtrl.GetItemText(self.PluginsTreeCtrl.GetRootItem()))
        tree_root = self.PluginsTreeCtrl.AddRoot("Plugins")
        for cat in self.__loaded_plugins:
            cat_id = self.PluginsTreeCtrl.AppendItem(tree_root, cat)

            # Add each plugin under cat
            for plugin in self.__loaded_plugins[cat]:
                self.PluginsTreeCtrl.AppendItem(cat_id, plugin.get_name())


    def __set_status_bar_message(self, message):
        '''
        Sets the status bar text to message
        @param message: The message to set
        '''

        # Check len
        if len(message) > 40:
            message = message[:37] + "..."

        self.StatusBar.SetStatusText(message)


    def __create_new_plugin(self, event):
        '''
        Creates Space for a new plugin
        @param event:
        @return:
        '''


        # Where should this plugin be placed on the treectrl? Maybe we need a separate dialog and not a button
        # New plugin button can be a Delete plugin button
        new_plugin_dialog = _NewPluginDialog(self, self.__plugins_home_dir, self.__sdk)
        new_plugin_dialog.Show()




    def __set_selected_plugin(self, event):
        '''
        Sets the selected plugin and updates the GUI
        @return:
        '''

        # Get plugin name and cat and set obj
        selected_plugin_name = self.PluginsTreeCtrl.GetItemText(self.PluginsTreeCtrl.GetSelection())
        # If plugin selected and not category
        if selected_plugin_name.lower() != "core" and selected_plugin_name.lower() != "addon":
            self.__selected_plugin = self.__loaded_plugins
            selected_plugin_cat = self.PluginsTreeCtrl.GetItemText(
                self.PluginsTreeCtrl.GetItemParent(self.PluginsTreeCtrl.GetSelection())
            )

            self.PluginNameTextCtrl.SetValue(selected_plugin_name)
            self.PluginTypeComboBox.SetValue(selected_plugin_cat)

        else:

            self.PluginNameTextCtrl.SetValue("")
            self.PluginTypeComboBox.SetValue("core")


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
        self.__plugins_home_dir = None
        PluginsHomeDirDialog.__init__(self, parent=self.__parent)

        # Set events
        self.__set_events()


    def __set_events(self):
        '''
        Set events
        @return:
        '''

        self.Bind(wx.EVT_BUTTON, self.__set_plugins_home, self.OkCancelSizerOK)
        self.Bind(wx.EVT_BUTTON, self.__cancel, self.OkCancelSizerCancel)


    def __set_plugins_home(self, event):
        '''
        Sets the plugins home, loads plugins and closes dialog
        @return:
        '''

        # Validate path
        plugins_path = self.PluginsHomeDirPicker.GetPath()
        if not plugins_path or not os.path.isdir(plugins_path):
            self.StatusLabel.SetLabel("Valid path must be specified")
            return

        # Get plugin home directory
        self.__plugins_home_dir = self.PluginsHomeDirPicker.GetPath()

        # Load plugins

        # Hide dialog
        self.Hide()
        self.__parent.Enable()
        self.__parent.Raise()

        # Load plugins
        self.__parent.set_plugins_home(self.__plugins_home_dir)


    def Show(self):
        '''
        Shows
        @return:
        '''

        # Disable Parent Window
        self.__parent.Disable()
        super(_PluginsHomeDirDialog, self).Show()


    def __cancel(self, event):
        '''
        Bound to cancel Button. Closes entire app
        @todo: Only Destroy everything if we're not changing the path
        @param event:
        @return:
        '''

        self.__parent.Destroy()
        self.Destroy()



class _NewPluginDialog(NewPluginDialog):
    ''''
    New Plugin Dialog box for creating a new plugin
    '''

    PLUGIN_NAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z_]{3,20}$")


    def __init__(self, parent, plugins_home_dir, sdk):
        '''
        Constructor
        @param plugins_home_dir: Plugins home dir
        @param parent: Parent object
        @param sdk: SDK object
        '''
        self.__parent = parent
        self.__sdk = sdk
        self.__plugins_home_dir = plugins_home_dir
        NewPluginDialog.__init__(self, parent=self.__parent)

        # Bind events
        self.__set_events()

        # Disable parent
        self.__parent.Disable()


    def __set_events(self):
        '''
        Bind events
        @return:
        '''

        self.Bind(wx.EVT_BUTTON, self.__create_new_plugin, self.OkCanelSizerOK)
        self.Bind(wx.EVT_BUTTON, self.__cancel, self.OkCanelSizerCancel)


    def __create_new_plugin(self, event):
        '''
        Save the plugin
        @param event:
        @return:
        '''

        # Handle inputs
        name = self.PluginNameTextCtrl.GetValue()
        _type = self.PluginTypeChoice.GetString(self.PluginTypeChoice.GetSelection())

        # Check plugin name
        if not self.PLUGIN_NAME_REGEX.match(name):
            self.StatusLabel.SetLabelText("Error: Invalid plugin name. Must be alphanumeric and 4-20 characters long")
            return

        # Create plugin
        self.__sdk.create_plugin(_type, name)
        self.__parent.reload_plugins()


    def __cancel(self, event):
        '''
        Cancels plugin creation and re-enables Main GUI
        @return: 
        '''

        self.__parent.Enable()
        self.Destroy()





