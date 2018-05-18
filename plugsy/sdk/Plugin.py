'''
Plugin Class - Holds methods for creating, deleting and editing a plugiin
'''

# Import libs
import os
import shutil
import importlib

# Import package modules
from .Exceptions import *
from ..Exceptions import *
from .. import Config
from ..Logger import Logger

class Plugin(Logger):
    '''
    Represent a plugin object
    '''

    TEMPLATE_PLUGIN_NAME = "PluginTemplate"

    def __init__(self, plugins_dir_path, name, plugin_type=None):
        '''
        Constructor

        :param plugins_dir_path: Path of the target plugins folder
        :param name: The name of the plugin object
        :param plugin_type: Optional plugin type. Used only when a pluign is being created
        '''
        Logger.__init__(
            self,
            name="%s.sdk.%s.%s" % (Config.FULL_NAME, self.__class__.__name__, name)
        )
        self.logger.debug("ENTRY")
        self.__plugins_dir_path = plugins_dir_path
        self.__name = name
        self.__home = None
        self.__is_core_plugin = None

        # Set plugin type
        if plugin_type is not None:
            if plugin_type.lower() == "core":
                self.logger.debug("Setting plugin as core")
                self.__is_core_plugin = True
            elif plugin_type.lower() == "addon":
                self.logger.debug("Setting plugin as addon")
                self.__is_core_plugin = False

        # Load plugin config
        if plugin_type is not None and self.does_plugin_exist():
            self.logger.debug("Plugin '%s' already exists. Loading" % self.__name)
            self.__load_plugin_config()

        self.logger.debug("EXIT")


    def create(self):
        '''
        Creates the plugin
        '''
        self.logger.debug("ENTRY")

        # Check core plugin is set
        if self.__is_core_plugin is None:
            self.logger.error("Cannot create new plugin. Type not set")
            raise PluginTypeNotSet()

        # Check plugin doesn't exist
        if self.does_plugin_exist():
            self.logger.error("Cannot create new plugin. Plugin already exists")
            raise PluginAlreadyExists(self.__name)

        # Set home
        if self.__is_core_plugin:
            self.__home = os.path.join(self.__plugins_dir_path, "core", self.__name)
        else:
            self.__home = os.path.join(self.__plugins_dir_path, "addon", self.__name)
        self.logger.debug("Plugin home set as '%s'" % self.__home)

        # Create home
        try:
            os.makedirs(self.__home)
        except FileExistsError:
            self.logger.error("Cannot create new plugin. Plugin home directory already exists")
            raise PluginCreationFailure(self.__name, "The directory at '%s' already exists" % self.__home)

        # Add plugin package files
        self.__create_init()
        self.__create_config()
        self.__create_class_file()

        self.logger.info("Plugin '%s' created at '%s'" % (self.__name, self.__home))
        self.logger.debug("EXIT")


    def does_plugin_exist(self):
        '''
        Checks if the plugin exists

        :return: True if the plugin exists, otherwise False
        '''
        self.logger.debug("ENTRY")

        # Check core
        plugin_path = os.path.join(self.__plugins_dir_path, "core", self.__name)
        if os.path.isdir(plugin_path):
            self.logger.debug("EXIT with True (core)")
            return True

        # Check addon
        plugin_path = os.path.join(self.__plugins_dir_path, "addon", self.__name)
        if os.path.isdir(plugin_path):
            self.logger.debug("EXIT with True (addon)")
            return True

        self.logger.debug("EXIT with False")
        return False


    def delete(self):
        '''
        Deletes the plugin
        '''
        self.logger.debug("ENTRY")

        # Check plugin exists
        if not self.does_plugin_exist():
            self.logger.error("Cannot delete plugin. Plugin does not exist")
            raise PluginDoesNotExist(self.__name)

        # Set plugin type
        if self.__is_core_plugin is None:
            # Check core
            if os.path.isdir(os.path.join(self.__plugins_dir_path, "core", self.__name)):
                self.__is_core_plugin = True
            # Check addon
            elif os.path.isdir(os.path.join(self.__plugins_dir_path, "addon", self.__name )):
                self.__is_core_plugin = False

        # Set home
        if self.__is_core_plugin:
            self.__home = os.path.join(self.__plugins_dir_path, "core", self.__name)
        else:
            self.__home = os.path.join(self.__plugins_dir_path, "addon", self.__name)
        self.logger.debug("Plugin exists at '%s'" % self.__home)

        shutil.rmtree(self.__home)
        self.logger.debug("EXIT")


    def __create_init(self):
        '''
        Creates the Plugin __init__.py
        '''
        self.logger.debug("ENTRY")
        template_path = os.path.join(os.path.dirname(__file__), self.TEMPLATE_PLUGIN_NAME, "__init__.py")

        # Read init
        with open(template_path, "r") as template:
            new_init_contents = template.read().replace(self.TEMPLATE_PLUGIN_NAME, self.__name)

        # Write init
        with open(os.path.join(self.__home, "__init__.py"), "w") as new_init_file:
            new_init_file.write(new_init_contents)

        self.logger.debug("EXIT")


    def __create_config(self):
        '''
        Create the plugins Config.py
        '''
        self.logger.debug("ENTRY")
        template_path = os.path.join(os.path.dirname(__file__), self.TEMPLATE_PLUGIN_NAME, "Config.py")

        # Read config
        with open(template_path, "r") as template:
            new_config_contents = template.read().replace(self.TEMPLATE_PLUGIN_NAME, self.__name)

        # Write config
        with open(os.path.join(self.__home, "Config.py"), "w") as new_config_file:
            new_config_file.write(new_config_contents)

        self.logger.debug("EXIT")


    def __create_class_file(self):
        '''
        Creates the main class file of the Plugin
        '''
        self.logger.debug("ENTRY")
        template_path = os.path.join(os.path.dirname(__file__), self.TEMPLATE_PLUGIN_NAME, "%s.py" % self.TEMPLATE_PLUGIN_NAME)

        # Read plugin class
        with open(template_path, "r") as template:
            new_class_contents = template.read().replace(self.TEMPLATE_PLUGIN_NAME, self.__name)

        # Write plugin class
        with open(os.path.join(self.__home, "%s.py" % self.__name), "w") as new_class_file:
            new_class_file.write(new_class_contents)

        self.logger.debug("EXIT")

    def __load_plugin_config(self):
        '''
        Loads the plugin config contents
        '''
        self.logger.debug("ENTRY")

        # Set subpackage name
        if self.__is_core_plugin:
            subpackage = "core"
        else:
            subpackage = "addon"


        config_import = importlib.import_module("%s.%s.%s" % (
            subpackage,
            self.get_name(),
            "Config"
        ))

        self.logger.debug("EXIT")



    #############
    ## GETTERS ##
    #############
    def get_name(self):
        '''
        Get's plugin name

        :return: Plugin name
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("EXIT")
        return self.__name

    def get_description(self):
        '''
        Get's plugin description

        :return: Plugin description
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("EXIT")
        return self.__description

    def get_version(self):
        '''
        Get's plugin version

        :return: Plugin version
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("EXIT")
        return self.__version

    def get_author(self):
        '''
        Get's plugin author

        :return: Plugin author
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("EXIT")
        return self.__author

    def get_dependencies(self):
        '''
        Get's plugin dependencies

        :return: Plugin dependencies
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("EXIT")
        return self.__dependencies


    def get_home(self):
        '''
        Gets the plugin's home dir path

        :return: Home dir
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("EXIT")
        return self.__home

    def is_core_plugin(self):
        '''
        Get's plugin core status

        :return: True or False
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("EXIT")
        return self.__is_core_plugin


    #############
    ## SETTERS ##
    #############
    def set_core_plugin(self, core):
        '''
        For setting the plugin as core or not core

        :param core: True of False
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("Setting plugin as core: %s" % core)

        if core:
            self.__is_core_plugin = True
        else:
            self.__is_core_plugin = False

        # Set home
        if core:
            self.__home = os.path.join(self.__plugins_dir_path, "core", self.__name)
        else:
            self.__home = os.path.join(self.__plugins_dir_path, "addon", self.__name)

        self.logger.debug("Plugin home set to '%s'" % self.__home)

        self.logger.debug("EXIT")
