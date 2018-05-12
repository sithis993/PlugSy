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
from .ConfirmationDialogs import *
from ..Sdk import Sdk
from ..Exceptions import *
from ...Plugsy import Plugsy
from ... import Config
from ...Logger import Logger


# ======================================
# = SdkGui Class
# ======================================
class SdkGui(MainFrame):
    '''
    SDK Gui - Main
    @todo: Add debug
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__sdk = None
        self.__plugins_home_dir = None
        self.plugins_tree = None
        self.__loaded_plugins = {}
        self.__selected_plugin = None
        self.__log_level = ""
        self.__log_path = ""
        MainFrame.__init__(self, parent=None)

        # Update visuals
        self.__update_visuals()

        # Bind plugin events
        self.__set_events()

        # Open Plugin home dir dialog
        self.__plugins_home_dir_dialog = _PluginsHomeDirDialog(parent=self)
        self.__plugins_home_dir_dialog.Show()


    def __update_visuals(self):
        '''
        Apply any post init visual changes
        @return:
        '''

        # Update title
        self.SetTitle("PlugSy - %s" % Config.VERSION)


    def __set_events(self):
        '''
        Set GUI event handlers
        @return:
        '''

        # Keyboard shortcut IDs
        new_plugin_id = wx.NewId()

        # Bind events
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.__set_selected_plugin, self.PluginsTreeCtrl)
        self.Bind(wx.EVT_BUTTON, self.__delete_plugin, self.DeletePluginButton)
        self.Bind(wx.EVT_MENU, self.__create_new_plugin, self.NewPluginMenuItem)
        self.Bind(wx.EVT_MENU, self.__create_new_plugin, id=new_plugin_id)
        self.Bind(wx.EVT_MENU, self.__close, self.ExitMenuItem)

        # Set shortcuts (accelerators)
        accelerator_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord("N"), new_plugin_id)
        ])
        self.SetAcceleratorTable(accelerator_tbl)


    def reload_plugins(self):
        '''
        Reloads plugins from specified plugins home directory
        @return:
        '''
        self.logger.debug("reload_plugins(): ENTRY")

        self.__loaded_plugins = self.__sdk.get_plugins()
        self.logger.info("reload_plugins(): Loaded '%s' core plugins" % len(self.__loaded_plugins["core"]))
        self.logger.info("reload_plugins(): Loaded '%s' addon plugins" % len(self.__loaded_plugins["addon"]))
        self.plugins_tree.populate_tree(self.__loaded_plugins)

        self.logger.debug("reload_plugins(): ENTRY")


    def __create_new_plugin(self, event):
        '''
        Open Plugin Creation Dialog
        @param event:
        @return:
        '''
        self.logger.debug("__create_new_plugin(): ENTRY")

        new_plugin_dialog = _NewPluginDialog(self, self.__plugins_home_dir, self.__sdk)
        new_plugin_dialog.Show()

        self.logger.debug("__create_new_plugin(): EXIT")


    def __delete_plugin(self, event):
        '''
        Open Plugin Creation Deletion
        @return:
        '''
        self.logger.debug("__delete_plugin(): ENTRY")
        plugin_name = self.plugins_tree.get_current_selection_text()
        self.logger.debug("__delete_plugin(): Attempting to delete '%s' plugin" % plugin_name)

        delete_plugin_dialog = DeletePluginConfirmation(self, plugin_name, self.__sdk)
        delete_plugin_dialog.Show()

        self.logger.debug("__delete_plugin(): EXIT")


    def sync_config_fields(self):
        '''
        Syncs config fields so they are that of the currently selected tree item
        @return:
        '''

        self.__set_selected_plugin(None)


    def clear_config_fields(self):
        '''
        Convenience method to clear all configuration boxes and items and reset to default
        @return:
        '''
        self.logger.debug("clear_config_fields(): ENTRY")

        self.PluginNameTextCtrl.SetValue("")
        self.PluginTypeComboBox.SetValue("core")
        self.DeletePluginButton.Disable()

        self.logger.debug("clear_config_fields(): EXIT")


    def __close(self, event):
        '''
        Event handler method for closing the application
        @param event:
        @return:
        '''

        self.Destroy()

    #############
    ## SETTERS ##
    #############

    def set_plugins_home(self, plugins_home_dir):
        '''
        Sets the plugins home dir to the specified directory and loads contained plugins
        @param plugins_home_dir: Absolute path to the plugins home
        @return:
        '''
        self.__plugins_home_dir = plugins_home_dir

        # Init SDK and load plugins
        self.__sdk = Sdk(plugins_home_dir, self.__log_level, self.__log_path)
        self.__loaded_plugins = self.__sdk.get_plugins()

        # Init logger
        Logger.__init__(
            self,
            name="%s.sdk.SdkGui" % Config.FULL_NAME
        )
        self.logger.debug("set_plugins_home(): Setting plugins home to '%s'" % plugins_home_dir)
        self.logger.info("set_plugins_home(): Loaded '%s' core plugins" % len(self.__loaded_plugins["core"]))
        self.logger.info("set_plugins_home(): Loaded '%s' addon plugins" % len(self.__loaded_plugins["addon"]))
        self.plugins_tree = PluginTree(self.PluginsTreeCtrl, self.__loaded_plugins)


        # Set status bar
        self.__set_status_bar_message("Plugins Home - %s" % plugins_home_dir)
        self.__sdk.test_plugsy()
        self.logger.debug("set_plugins_home(): EXIT")


    def __set_status_bar_message(self, message):
        '''
        Sets the status bar text to message
        @param message: The message to set
        '''
        self.logger.debug("__set_status_bar_message(): ENTRY")
        self.logger.debug("__set_status_bar_message(): Setting message as '%s'" % message)

        # Check len
        if len(message) > 40:
            message = message[:37] + "..."

        self.StatusBar.SetStatusText(message)
        self.logger.debug("__set_status_bar_message(): EXIT")


    def __set_selected_plugin(self, event):
        '''
        Sets the selected plugin and updates the GUI
        @return:
        '''
        self.logger.debug("__set_selected_plugin(): ENTRY")

        # Get plugin name and cat and set obj
        selected_plugin_name = self.plugins_tree.get_current_selection_text()
        self.logger.debug("__set_selected_plugin(): Setting selected plugin to '%s'" % selected_plugin_name)
        # If plugin selected and not category
        if selected_plugin_name.lower() != "core" and selected_plugin_name.lower() != "addon":
            self.__selected_plugin = self.__loaded_plugins
            selected_plugin_cat = self.PluginsTreeCtrl.GetItemText(
                self.PluginsTreeCtrl.GetItemParent(self.plugins_tree.get_current_selection_id())
            )

            self.PluginNameTextCtrl.SetValue(selected_plugin_name)
            self.PluginTypeComboBox.SetValue(selected_plugin_cat)
            self.DeletePluginButton.Enable()

        else:

            self.logger.debug(
                "__set_selected_plugin(): Category '%s' selected. Clearing config fields" %
                selected_plugin_name
            )
            self.clear_config_fields()

        self.logger.debug("__set_selected_plugin(): EXIT")


    def set_log_level(self, log_level):
        '''
        Sets log level
        @param log_level:
        @return:
        '''

        self.__log_level = log_level


    def set_log_path(self, log_path):
        '''
        Sets the log path
        @param log_path:
        @return:
        '''

        self.__log_path = log_path



# ======================================
# = _PluginsHomeDirDialog Class
# ======================================
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

        # Disable log file path
        self.LogFilePathTextCtrl.Disable()


    def Show(self):
        '''
        Shows
        @return:
        '''

        # Disable Parent Window
        self.__parent.Disable()
        super(_PluginsHomeDirDialog, self).Show()


    def __update_choice(self, event):
        '''
        Triggered when the Log level choice box is altered. For controlling GUI based upon selection
        @param event:
        @return:
        '''
        log_level = self.LogLevelChoice.GetString(self.LogLevelChoice.GetSelection())

        # Enable Log file path text ctrl if log level not none
        if log_level:
            self.LogFilePathTextCtrl.Enable()
        else:
            self.LogFilePathTextCtrl.Disable()

        # If debug selected, display warning, otherwise clear it
        if log_level.lower() == "debug":
            self.__set_status_message("Setting Log Level to Debug may severely impact performance", "warning")
        else:
            self.__clear_status_message()


    def __cancel(self, event):
        '''
        Bound to cancel Button. Closes entire app
        @param event:
        @return:
        '''

        self.__parent.Destroy()
        self.Destroy()

    #############
    ## SETTERS ##
    #############

    def __set_events(self):
        '''
        Set events
        @return:
        '''

        self.Bind(wx.EVT_BUTTON, self.__set_plugins_home, self.OkCancelSizerOK)
        self.Bind(wx.EVT_BUTTON, self.__cancel, self.OkCancelSizerCancel)
        self.Bind(wx.EVT_CHOICE, self.__update_choice, self.LogLevelChoice)


    def __set_plugins_home(self, event):
        '''
        Sets the plugins home, loads plugins and closes dialog
        @return:
        '''

        # Validate path
        plugins_path = self.PluginsHomeDirPicker.GetPath()
        if not plugins_path or not os.path.isdir(plugins_path):
            self.__set_status_message("Valid path must be specified", "error")
            return

        # Validate Debug settings
        log_level = self.LogLevelChoice.GetString(self.LogLevelChoice.GetSelection())
        log_path = self.LogFilePathTextCtrl.GetValue()
        if log_level:
            # If log file exists, show Confirmation
            if os.path.isfile(log_path):
                confirmation_box = GenericConfirmationDialog(
                    self, "The log file at '%s' already exists. Do you want to overwrite it?"
                )
                confirmation_box.ShowModal()
                if not confirmation_box.was_accepted():
                    return

        # Get plugin home directory
        self.__plugins_home_dir = self.PluginsHomeDirPicker.GetPath()

        # Hide dialog
        self.Hide()
        self.__parent.Enable()
        self.__parent.Raise()

        # Set logger config
        self.__parent.set_log_level(log_level)
        self.__parent.set_log_path(log_path)

        # Load plugins
        self.__parent.set_plugins_home(self.__plugins_home_dir)


    def __set_status_message(self, message, _type):
        '''
        Sets the status message
        @param message: The message string to set
        @param _type: The type of message. should be error or warning
        @return:
        '''
        message_prefix = ""

        if _type.lower() == "error":
            self.StatusLabel.SetForegroundColour(wx.Colour(255, 0, 0))
            message_prefix = "Error: "
        elif _type.lower() == "warning":
            self.StatusLabel.SetForegroundColour(wx.Colour(255, 128, 0))
            message_prefix = "Warning: "

        self.StatusLabel.SetLabel(message_prefix + message)


    def __clear_status_message(self):
        '''
        Clears the status message area
        @return:
        '''

        self.StatusLabel.SetLabel("")


# ======================================
# = NewPluginDialog Class
# ======================================
class _NewPluginDialog(NewPluginDialog):
    ''''
    New Plugin Dialog box for creating a new plugin
    @todo: Add debug
    '''

    PLUGIN_NAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z_]{2,20}$")
    RESERVED_PLUGIN_NAMES = ["core", "addon"]


    def __init__(self, parent, plugins_home_dir, sdk):
        '''
        Constructor
        @param plugins_home_dir: Plugins home dir
        @param parent: Parent object
        @param sdk: SDK object
        '''
        #self.logger = Logger(
        #    "%s.sdk.gui.%s" % (Config.FULL_NAME, self.__class__.__name__),
        #    parent.log_level, parent.log_path
        #)
        #self.logger.debug("__init__(): ENTRY")
        self.__parent = parent
        self.__sdk = sdk
        self.__plugins_home_dir = plugins_home_dir
        NewPluginDialog.__init__(self, parent=self.__parent)

        # Bind events
        self.__set_events()

        # Disable parent
        self.__parent.Disable()
        #self.logger.debug("__init__(): EXIT")


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

        # Check plugin doesn't already exist
        if self.__sdk.does_plugin_exist(name):
            self.StatusLabel.SetLabelText("Error: A plugin with the specified name already exists")
            return

        # Check plugin name isn't reserved
        if name.lower() in self.RESERVED_PLUGIN_NAMES:
            self.StatusLabel.SetLabelText("Error: Plugin name is reserved. Please choose another name")
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

    #############
    ## SETTERS ##
    #############

    def __set_events(self):
        '''
        Bind events
        @return:
        '''

        self.Bind(wx.EVT_BUTTON, self.__create_new_plugin, self.OkCanelSizerOK)
        self.Bind(wx.EVT_BUTTON, self.__cancel, self.OkCanelSizerCancel)


# ======================================
# = PluginTree Class
# ======================================
class PluginTree():
    '''
    Represents the wx TreeCtrl for the SDK Plugins. Provides convenience methods
    for getting tree items, adding items to the tree, checking for item presence etc.
    @todo: Add debug
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
            # if cat in get_list_of_category_names() (children under the root node)
            if cat not in self.get_category_names():
                self.__tree.AppendItem(self.__root, cat)

            # Add each plugin under cat
            for plugin in loaded_plugins[cat]:
                if plugin.get_name() not in self.get_category_plugin_names(cat):
                    self.__tree.AppendItem(self.__get_category_id(cat), plugin.get_name())


    def remove_plugin(self):
        '''
        Removes the currently selected plugin item from the tree
        @return:
        '''

        plugin_id = self.get_current_selection_id()
        self.__tree.Delete(plugin_id)

    #############
    ## GETTERS ##
    #############

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

    def get_category_plugin_names(self, category_name):
        '''
        Fetches a list of the plugin names under a specific category (root child)
        @param category_name: The category name of which to get plugin names
        @return: A list of the plugin names under the cat
        '''
        plugin_names = []
        cat_id = self.__get_category_id(category_name)

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

    def get_current_selection_text(self):
        '''
        Gets the text of the currently selected tree item
        @return: string
        '''

        selected_plugin_name = self.__tree.GetItemText(self.__tree.GetSelection())

        return selected_plugin_name


    def get_current_selection_id(self):
        '''
        Gets the id of the currently selected tree item
        @return: id object
        '''

        selected_plugin_id = self.__tree.GetSelection()

        return selected_plugin_id

    #############
    ## SETTERS ##
    #############


    def set_focus_by_id(self, item_id):
        '''
        Sets the tree's current focus to item specified by ID
        @param item_id: The ID of the item to focus on
        @return:
        '''

        self.__tree.SetFocusedItem(item_id)

