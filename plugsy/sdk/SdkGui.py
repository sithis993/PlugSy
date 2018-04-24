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
        self.__plugins_tree = None
        self.__loaded_plugins = {}
        self.__selected_plugin = None
        MainFrame.__init__(self, parent=None)

        # Bind plugin events
        self.__set_events()

        # Open Plugin home dir dialog
        self.__plugins_home_dir_dialog = _PluginsHomeDirDialog(parent=self)
        self.__plugins_home_dir_dialog.Show()

        # Init plugins tree object
        self.__plugins_tree = None


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
        #self.set_plugins_home(self.__plugins_home_dir)

        self.__loaded_plugins = self.__sdk.get_plugins()
        self.__plugins_tree.populate_tree(self.__loaded_plugins)



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
        self.__plugins_tree = PluginTree(self.PluginsTreeCtrl, self.__loaded_plugins)

        # Set status bar
        self.__set_status_bar_message("Plugins Home - %s" % plugins_home_dir)


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

        # Close
        self.__parent.Enable()
        self.Destroy()


    def __cancel(self, event):
        '''
        Cancels plugin creation and re-enables Main GUI
        @return: 
        '''

        self.__parent.Enable()
        self.Destroy()



class PluginTree():
    '''
    Represents the wx TreeCtrl for the SDK Plugins. Provides convenience methods
    for getting tree items, adding items to the tree, checking for item presence etc.
    '''


    def __init__(self, tree, loaded_plugins):
        '''
        Constructor
        @param tree: Handle to the wx TreeCtrl object
        '''
        self.__tree = tree
        self.__categories = []
        self.__loaded_plugins = loaded_plugins

        # setup tree
        self.__root = self.__tree.AddRoot("Plugins")

        # Populate
        self.populate_tree(loaded_plugins)


    def populate_tree(self, loaded_plugins):
        '''
        Populates the tree ctrl with loaded pluginss
        @param loaded_plugins: List of loaded plugin objects
        @return:
        '''

        for cat in loaded_plugins:
            # if cat in get_list_of_categiry_names() (children under the root node)
            if cat not in self.get_category_names():
                self.__tree.AppendItem(self.__root, cat)

            # Add each plugin under cat
            for plugin in loaded_plugins[cat]:
                if plugin.get_name() not in self.get_category_plugin_names(cat):
                    self.__tree.AppendItem(self.__get_category_id(cat), plugin.get_name())


    def get_category_names(self):
        '''
        Fetches a list of the neames of categories in the Plugin tree ctrl
        @return: List of strings
        '''
        category_names = []

        # Get first child
        category, cookie = self.__tree.GetFirstChild(self.__root)

        # Iterate remaining children
        while category.IsOk():
            category_names.append(self.__tree.GetItemText(category))
            category, cookie = self.__tree.GetNextChild(self.__root, cookie)

        return category_names


    def __get_category_id(self, category_name):
        '''
        Fetches and returns the cateogyr ID object of a specifid category
        @param category: category name for which to return the ID object. If the category doesn't exist, then this will
        be None
        @return: id object or None
        @todo TEST
        '''
        category_id = None

        category, cookie = self.__tree.GetFirstChild(self.__root)

        # Iterate categories
        while category.IsOk() and self.__tree.GetItemText(category) != category_name:
            category, cookie = self.__tree.GetNextChild(self.__root, cookie)

        # Check category name
        if self.__tree.GetItemText(category) == category_name:
            category_id = category

        return category_id

    def get_category_plugin_names(self, category):
        '''
        Fetches a list of the plugin names under a specific category (root child)
        @param category: The category of which to get plugin names
        @return: A list of the plugin names under the cat
        '''
        plugin_names = []
        cat_id = self.__get_category_id(category)

        plugin_id, cookie = self.__tree.GetFirstChild(cat_id)

        # Iterate plugins
        while plugin_id.IsOk():
            plugin_names.append(self.__tree.GetItemText(plugin_id))
            plugin_id, cookie = self.__tree.GetNextChild(cat_id, cookie)

        return plugin_names


    def __get_category_plugin_ids(self, category):
        '''
        Fetches a list of the plugin ids under a specific category (root child)
        @param category: The category of which to get plugin ids
        @return: A list of the plugin ids under the cat
        '''

        pass
