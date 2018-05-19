'''
PlugSy - SDK Gui
'''

# Import libs
import os
import re
from .SdkGuiAbs import PluginsHomeDirDialog
from .SdkGuiAbs import MainFrame
from .SdkGuiAbs import NewPluginDialog
from .ConfirmationDialogs import *
from ..Sdk import Sdk
from ... import Config
from ...utils import Logger


# ======================================
# = SdkGui Class
# ======================================
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
        '''

        # Update title
        self.SetTitle("PlugSy - %s" % Config.VERSION)


    def __set_events(self):
        '''
        Set GUI event handlers
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
        '''
        self.logger.debug("ENTRY")

        self.__loaded_plugins = self.__sdk.get_plugins()
        self.logger.info("Loaded '%s' core plugins" % len(self.__loaded_plugins["core"]))
        self.logger.info("Loaded '%s' addon plugins" % len(self.__loaded_plugins["addon"]))
        self.plugins_tree.populate_tree(self.__loaded_plugins)

        self.logger.debug("EXIT")


    def __create_new_plugin(self, event):
        '''
        Open Plugin Creation Dialog

        :param event: wx event object
        '''
        self.logger.debug("ENTRY")

        new_plugin_dialog = _NewPluginDialog(self, self.__plugins_home_dir, self.__sdk)
        new_plugin_dialog.Show()

        self.logger.debug("EXIT")


    def __delete_plugin(self, event):
        '''
        Open Plugin Creation Deletion

        :param event: wx event object
        '''
        self.logger.debug("ENTRY")
        plugin_name = self.plugins_tree.get_current_selection_text()
        self.logger.debug("Attempting to delete '%s' plugin" % plugin_name)

        delete_plugin_dialog = DeletePluginConfirmation(self, plugin_name, self.__sdk)
        delete_plugin_dialog.Show()

        self.logger.debug("EXIT")


    def sync_config_fields(self):
        '''
        Syncs config fields so they are that of the currently selected tree item
        '''
        self.logger.debug("ENTRY")

        self.__set_selected_plugin(None)
        self.logger.debug("EXIT")


    def clear_config_fields(self):
        '''
        Convenience method to clear all configuration boxes and items and reset to default
        '''
        self.logger.debug(" ENTRY")

        self.PluginNameTextCtrl.SetValue("")
        self.PluginTypeComboBox.SetValue("core")
        self.DeletePluginButton.Disable()

        self.logger.debug("EXIT")


    def __close(self, event):
        '''
        Event handler method for closing the application

        :param event: wx event object
        '''

        self.Destroy()

    #############
    ## SETTERS ##
    #############

    def set_plugins_home(self, plugins_home_dir):
        '''
        Sets the plugins home dir to the specified directory and loads contained plugins

        :param plugins_home_dir: Absolute path to the plugins home
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
        self.logger.debug("Plugins home set to '%s'" % plugins_home_dir)
        self.logger.info("Loaded '%s' core plugins" % len(self.__loaded_plugins["core"]))
        self.logger.info("Loaded '%s' addon plugins" % len(self.__loaded_plugins["addon"]))

        # Add plugins to tree
        self.plugins_tree = PluginTree(self.PluginsTreeCtrl, self.__loaded_plugins)

        # Set status bar
        self.__set_status_bar_message("Plugins Home - %s" % plugins_home_dir)
        self.logger.debug("EXIT")


    def __set_status_bar_message(self, message):
        '''
        Sets the status bar text to message. Truncates if necessary

        :param message: The message to set in the wx status bar
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("Setting message as '%s'" % message)

        # Check len
        if len(message) > 40:
            message = message[:37] + "..."

        self.StatusBar.SetStatusText(message)
        self.logger.debug("EXIT")


    def __set_selected_plugin(self, event):
        '''
        Sets the selected plugin and updates the GUI

        :param event: wx event object
        '''
        self.logger.debug("ENTRY")

        # Get plugin name and cat and set obj
        selected_plugin_name = self.plugins_tree.get_current_selection_text()
        self.logger.debug("Setting selected plugin to '%s'" % selected_plugin_name)
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
                "Category '%s' selected. Clearing config fields" %
                selected_plugin_name
            )
            self.clear_config_fields()

        self.logger.debug("EXIT")


    def set_log_level(self, log_level):
        '''
        Sets log level

        :param log_level: The log level
        '''

        self.__log_level = log_level


    def set_log_path(self, log_path):
        '''
        Sets the log path

        :param log_path: The log file path
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

        :param parent: Parent Window. SDK MainFrame in this case
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
        Shows the dialog
        '''

        # Disable Parent Window
        self.__parent.Disable()
        super(_PluginsHomeDirDialog, self).Show()


    def __update_choice(self, event):
        '''
        Triggered when the Log level choice box is altered. For controlling GUI based upon selection

        :param event: wx event object
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

        :param event: wx event object
        '''

        self.__parent.Destroy()
        self.Destroy()

    #############
    ## SETTERS ##
    #############

    def __set_events(self):
        '''
        Set events
        '''

        self.Bind(wx.EVT_BUTTON, self.__set_plugins_home, self.OkCancelSizerOK)
        self.Bind(wx.EVT_BUTTON, self.__cancel, self.OkCancelSizerCancel)
        self.Bind(wx.EVT_CHOICE, self.__update_choice, self.LogLevelChoice)


    def __set_plugins_home(self, event):
        '''
        Sets the plugins home, loads plugins and closes dialog

        :param event: wx event object
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
                    self, "The log file at '%s' already exists. Do you want to overwrite it?" % log_path
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

        :param message: The message string to set
        :param _type: The type of message. should be error or warning
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
        '''

        self.StatusLabel.SetLabel("")


# ======================================
# = NewPluginDialog Class
# ======================================
class _NewPluginDialog(NewPluginDialog, Logger):
    ''''
    New Plugin Dialog box for creating a new plugin
    '''

    PLUGIN_NAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z_]{2,20}$")
    RESERVED_PLUGIN_NAMES = ["core", "addon"]


    def __init__(self, parent, plugins_home_dir, sdk):
        '''
        Constructor

        :param parent: Parent object
        :param plugins_home_dir: Plugins home dir
        :param sdk: SDK object
        '''
        Logger.__init__(
            self,
            name="%s.sdk.%s" % (Config.FULL_NAME, self.__class__.__name__)
        )
        self.logger.debug("ENTRY")
        self.__parent = parent
        self.__sdk = sdk
        self.__plugins_home_dir = plugins_home_dir
        NewPluginDialog.__init__(self, parent=self.__parent)

        # Bind events
        self.__set_events()

        # Disable parent
        self.__parent.Disable()
        self.logger.debug("EXIT")


    def __create_new_plugin(self, event):
        '''
        Creates the plugin

        :param event: wx event object
        '''
        self.logger.debug("ENTRY")

        # Handle inputs
        name = self.PluginNameTextCtrl.GetValue()
        _type = self.PluginTypeChoice.GetString(self.PluginTypeChoice.GetSelection())
        self.logger.debug("Attempting creation of '%s' plugin of type '%s'" % (name, _type))

        # Check plugin name
        if not self.PLUGIN_NAME_REGEX.match(name):
            self.StatusLabel.SetLabelText("Error: Invalid plugin name. Must be alphanumeric and 4-20 characters long")
            self.logger.error(
                "The specified plugin name '%s' is invalid and does not match the regex '%s'." % (
                    name, self.PLUGIN_NAME_REGEX.pattern
                )
            )
            self.logger.debug("EXIT")
            return

        # Check plugin doesn't already exist
        if self.__sdk.does_plugin_exist(name):
            self.StatusLabel.SetLabelText("Error: A plugin with the specified name already exists")
            self.logger.error("A plugin already exists with the name '%s'" % name)
            self.logger.debug("EXIT")
            return

        # Check plugin name isn't reserved
        if name.lower() in self.RESERVED_PLUGIN_NAMES:
            self.StatusLabel.SetLabelText("Error: Plugin name is reserved. Please choose another name")
            self.logger.error("The keyword '%s' is reserved and cannot be used as a plugin name" % name)
            self.logger.debug("EXIT")
            return

        # Create plugin
        self.__sdk.create_plugin(_type, name)
        self.__parent.reload_plugins()

        # Close
        self.__parent.Enable()
        self.Destroy()
        self.logger.debug("EXIT")


    def __cancel(self, event):
        '''
        Cancels plugin creation and re-enables Main GUI

        :return: wx event object
        '''
        self.logger.debug("ENTRY")

        self.__parent.Enable()
        self.Destroy()

        self.logger.debug("EXIT")

    #############
    ## SETTERS ##
    #############

    def __set_events(self):
        '''
        Bind events
        '''
        self.logger.debug("ENTRY")

        self.Bind(wx.EVT_BUTTON, self.__create_new_plugin, self.OkCanelSizerOK)
        self.Bind(wx.EVT_BUTTON, self.__cancel, self.OkCanelSizerCancel)

        self.logger.debug("EXIT")


# ======================================
# = PluginTree Class
# ======================================
class PluginTree(Logger):
    '''
    Represents the wx TreeCtrl for the SDK Plugins. Provides convenience methods
    for getting tree items, adding items to the tree, checking for item presence etc.
    '''


    def __init__(self, tree, loaded_plugins):
        '''
        Constructor

        :param tree: Handle to the wx TreeCtrl object
        :param loaded_plugins: List of currently loaded plugin objects
        '''
        Logger.__init__(
            self,
            name="%s.sdk.%s" % (Config.FULL_NAME, self.__class__.__name__)
        )
        self.logger.debug("ENTRY")
        self.__tree = tree
        self.__categories = []
        self.__loaded_plugins = loaded_plugins

        # setup tree
        self.logger.debug("Adding root item to tree")
        self.__root = self.__tree.AddRoot("Plugins")

        # Populate
        self.logger.debug("Adding plugins to the tree")
        self.populate_tree(loaded_plugins)
        self.logger.debug("EXIT")


    def populate_tree(self, loaded_plugins):
        '''
        Populates the tree ctrl with loaded pluginss

        :param loaded_plugins: List of currently loaded plugin objects
        '''
        self.logger.debug("ENTRY")

        for cat in loaded_plugins:
            self.logger.debug("Adding '%s' plugins to tree" % cat)
            # if cat in get_list_of_category_names() (children under the root node)
            if cat not in self.get_category_names():
                self.logger.debug("'%s' category not yet in tree, adding it" % cat)
                self.__tree.AppendItem(self.__root, cat)

            # Add each plugin under cat
            self.logger.debug("Adding '%s' plugins to category" % len(loaded_plugins[cat]))
            for plugin in loaded_plugins[cat]:
                if plugin.get_name() not in self.get_category_plugin_names(cat):
                    self.logger.debug("Adding '%s' plugin to tree" % plugin.get_name())
                    self.__tree.AppendItem(self.__get_category_id(cat), plugin.get_name())

        self.logger.debug("EXIT")


    def remove_plugin(self):
        '''
        Removes the currently selected plugin item from the tree
        '''
        self.logger.debug("ENTRY")

        plugin_id = self.get_current_selection_id()
        self.debug("Removing '%s' plugin from tree" % self.get_current_selection_text())
        self.__tree.Delete(plugin_id)

        self.logger.debug("EXIT")


    #############
    ## GETTERS ##
    #############

    def get_category_names(self):
        '''
        Fetches a list of the names of categories in the Plugin tree ctrl

        :return: List of strings
        '''
        self.logger.debug("ENTRY")
        category_names = []

        # Get first child
        category, cookie = self.__tree.GetFirstChild(self.__root)

        # Iterate remaining children
        while category.IsOk():
            category_names.append(self.__tree.GetItemText(category))
            category, cookie = self.__tree.GetNextChild(self.__root, cookie)

        self.logger.debug("EXIT with '%s'" % category_names)
        return category_names


    def __get_category_id(self, category_name):
        '''
        Fetches and returns the category ID object of a specifid category

        :param category_name: category name for which to return the ID object. If the category doesn't exist, then
            this will be None
        :return: id object or None
        '''
        self.logger.debug("ENTRY")
        category_id = None

        category, cookie = self.__tree.GetFirstChild(self.__root)

        # Iterate categories
        while category.IsOk() and self.__tree.GetItemText(category) != category_name:
            category, cookie = self.__tree.GetNextChild(self.__root, cookie)

        # Check category name
        if self.__tree.GetItemText(category) == category_name:
            category_id = category

        self.logger.debug("EXIT with '%s'" % category_id)
        return category_id

    def get_category_plugin_names(self, category_name):
        '''
        Fetches a list of the plugin names under a specific category (root child)

        :param category_name: The category name of which to get plugin names
        :return: A list of the plugin names under the cat
        '''
        self.logger.debug("ENTRY")
        plugin_names = []
        cat_id = self.__get_category_id(category_name)

        plugin_id, cookie = self.__tree.GetFirstChild(cat_id)

        # Iterate plugins
        while plugin_id.IsOk():
            plugin_names.append(self.__tree.GetItemText(plugin_id))
            plugin_id, cookie = self.__tree.GetNextChild(cat_id, cookie)

        self.logger.debug("EXIT with '%s'" % plugin_names)
        return plugin_names


    def __get_category_plugin_ids(self, category):
        '''
        Fetches a list of the plugin ids under a specific category (root child)

        :param category: The category of which to get plugin ids
        :return: A list of the plugin ids under the cat
        '''
        self.logger.debug("ENTRY")

        pass
        self.logger.debug("EXIT")


    def get_current_selection_text(self):
        '''
        Gets the text of the currently selected tree item

        :return: the name string of the currently selected plugin
        '''
        self.logger.debug("ENTRY")

        selected_plugin_name = self.__tree.GetItemText(self.__tree.GetSelection())

        self.logger.debug("EXIT with '%s'" % selected_plugin_name)
        return selected_plugin_name


    def get_current_selection_id(self):
        '''
        Gets the id of the currently selected tree item

        :return: treectrl id object
        '''
        self.logger.debug("ENTRY")

        selected_plugin_id = self.__tree.GetSelection()

        self.logger.debug("EXIT with '%s'" % selected_plugin_id)
        return selected_plugin_id


    #############
    ## SETTERS ##
    #############

    def set_focus_by_id(self, item_id):
        '''
        Sets the tree's current focus to item specified by ID

        :param item_id: The ID of the item to focus on
        '''
        self.logger.debug("ENTRY")

        self.__tree.SetFocusedItem(item_id)

        self.logger.debug("EXIT")
