'''
Plugsy - Software Development Kit
'''

# Import libs
import os
import re
import sys
import importlib
import inspect

# Import package modules
from .Plugin import Plugin
from .Exceptions import *
from ..Exceptions import *
from ..Logger import Logger
from .. import Config
from ..Plugsy import Plugsy

class Sdk(Logger):
    '''
    SDK Class
    '''

    PLUGIN_NAME_REGEX = re.compile("^[a-zA-Z]+[a-zA-Z0-9_]*$")
    PLUGIN_NAME_MIN_LEN = 3
    PLUGIN_NAME_MAX_LEN = 35

    def __init__(self, plugins_home_path, debug_level="", debug_log_path=""):
        '''
        Constructor

        :param plugins_home_path: The path of the plugins package directory
        :param debug_level: Debug log level
        :param debug_log_path: Optional log file for debug
        '''
        # Init Plugsy and logger
        self.__plugsy = Plugsy(debug_level=debug_level, debug_log_path=debug_log_path)
        Logger.__init__(self, name="%s.sdk" % Config.FULL_NAME)
        self.logger.debug("ENTRY")

        self.__plugins = {}
        # Check plugins home exists
        if not os.path.isdir(plugins_home_path):
            raise PluginsHomeNotFound(plugins_home_path)

        self.logger.info("Setting plugins home to '%s'" % plugins_home_path)
        self.__plugins_dir_path = plugins_home_path

        self.__init_plugins_home()

        # Add plugins home dir to path
        sys.path.append(plugins_home_path)
        self.logger.debug("EXIT")


    def __init_plugins_home(self):
        '''
        Checks the plugin's home directory is initialised, or initialises if not. addon and core packages
        are created if they don't exist
        '''
        self.logger.debug("ENTRY")
        plugins_init_path = os.path.join(self.__plugins_dir_path, "__init__.py")
        addon_package_path = os.path.join(self.__plugins_dir_path, "addon")
        core_package_path = os.path.join(self.__plugins_dir_path, "core")

        # Create plugins home init
        if not os.path.isfile(plugins_init_path):
            self.logger.debug("__init__.py not found in plugins home dir. Creating it")
            with open(plugins_init_path, "w") as plugins_init_file:
                plugins_init_file.writelines([
                    "from . import core\n"
                    "from . import addon\n"
                    ]
                )

        # Create core and addon packages
        for package_path in [core_package_path, addon_package_path]:
            if not os.path.isdir(package_path):
                self.logger.debug("'%s' plugin package was not found in plugins home dir and will be created" %
                                  package_path
                                  )
                self.__create_bare_package(package_path)

        self.logger.debug("EXIT")


    def __create_bare_package(self, package_dir):
        '''
        Creates an empty, bare Python package at the specified location

        :param package_dir: The absolute path of the package to create
        '''
        self.logger.debug("ENTRY")
        init_path = os.path.join(package_dir, "__init__.py")

        # Create package dir
        if not os.path.isdir(package_dir):
            self.logger.debug("Creating package dir at '%s'" % package_dir)
            os.makedirs(package_dir)

        # Create empty __init__
        open(init_path, "w").close()
        self.logger.debug("__init__.py created at '%s'" % init_path)

        self.logger.debug("EXIT")


    def create_plugin(self, plugin_type, name):
        '''
        Creates a new plugin

        :param plugin_type: The type of plugin to create. Should be core or addon
        :param nane: The name of the plugin to create
        '''
        self.logger.debug("ENTRY")

        # Check name
        if not self.__is_valid_plugin_name(name):
            self.logger.error("Could not create plugin due to bad plugin name '%s'" % name)
            raise BadPluginName(name)
        # Check type
        if not self.__is_valid_plugin_type(plugin_type):
            self.logger.error("Could not create plugin due to bad plugin type '%s'" % plugin_type)
            raise BadPluginType(plugin_type)

        # Initiate plugin
        self.logger.info("Creating new '%s' plugin '%s'" % (plugin_type, name))
        new_plugin = Plugin(
            plugins_dir_path=self.__plugins_dir_path, name=name, plugin_type=plugin_type
        )

        # Create
        new_plugin.create()
        self.logger.info("Plugin creating successfully")

        # Add new plugin package to subpackage (core, addon) __init__
        self.__add_plugin_to_init(new_plugin)
        self.logger.debug("EXIT")


    def does_plugin_exist(self, plugin_name):
        '''
        Checks if a plugin exists with the specified name

        :param plugin_name: The name of the plugin to check for
        :return: True if plugin exists, otherwise False
        '''
        self.logger.debug("ENTRY")

        if not self.__plugins:
            self.get_plugins()

        for cat in self.__plugins:
            for plugin in self.__plugins[cat]:
                if plugin.get_name().lower() == plugin_name.lower():
                    self.logger.debug("EXIT with True")
                    return True

        self.logger.debug("EXIT with False")
        return False


    def delete_plugin(self, name):
        '''
        Deletes an existing plugin

        :param name: The name of the plugin to delete
        '''
        self.logger.debug("ENTRY")

        # Initiate plugin and delete
        existing_plugin = Plugin(self.__plugins_dir_path, name)
        existing_plugin.delete()
        self.logger.info("Plugin '%s' successfully deleted" % name)

        # Remove from init
        self.__remove_plugin_from_init(existing_plugin)
        self.logger.debug("EXIT")


    def __add_plugin_to_init(self, new_plugin):
        '''
        Adds the new plugin import to the relevant subpackage

        :param new_plugin: The name of the new plugin to add to the __init__ file
        '''
        self.logger.debug("ENTRY")

        init_contents = ""
        subpackage_init_path = os.path.join(
            self.__plugins_dir_path,
            "core" if new_plugin.is_core_plugin() else "addon",
            "__init__.py"
        )
        self.logger.debug("Adding plugin to init at '%s'" % subpackage_init_path)

        # Read subpackage init
        if os.path.isfile(subpackage_init_path):
            with open(subpackage_init_path, "r") as init_file:
                init_contents = init_file.read()

        # Add new Plugin package import
        if init_contents and not init_contents.endswith("\n") and not init_contents.endswith("\r"):
            init_contents += "\nfrom . import %s" % new_plugin.get_name()
        else:
            init_contents += "from . import %s\n" % new_plugin.get_name()

        # Write init
        with open(subpackage_init_path, "w") as init_file:
            init_file.write(init_contents)

        self.logger.debug("EXIT")


    def __remove_plugin_from_init(self, existing_plugin):
        '''
        Removes the Plugin package import from the subpackage __init__

        :param name: The name of the plugin to remove
        '''
        self.logger.debug("ENTRY")

        subpackage_init_path = os.path.join(
            self.__plugins_dir_path,
            "core" if existing_plugin.is_core_plugin() else "addon",
            "__init__.py"
        )
        self.logger.debug("Removing plugin from init at '%s'" % subpackage_init_path)

        if os.path.isfile(subpackage_init_path):
            # Read subpackage init
            with open(subpackage_init_path, "r") as init_file:
                init_contents = init_file.read()

            # Remove import
            init_contents = init_contents.replace("from . import %s\n" % existing_plugin.get_name(), "")

            # Write subpackage init
            with open(subpackage_init_path, "w") as init_file:
                init_file.write(init_contents)

        self.logger.debug("EXIT")

    #############
    ## GETTERS ##
    #############

    def get_plugins(self):
        '''
        Fetches current plugins in plugin home

        :return: Dict of core and addon plugin lists
        '''
        self.logger.debug("ENTRY")

        plugins = {
            "core": [],
            "addon": []
        }

        # Check for core and addon folders
        plugin_subdirs = os.listdir(self.__plugins_dir_path)
        for subpackage in ["core", "addon"]:
            if subpackage in plugin_subdirs:
                subpackage_path = os.path.join(self.__plugins_dir_path, subpackage)
                subpackage_import = importlib.reload(importlib.import_module(subpackage))

                for member in inspect.getmembers(subpackage_import):
                    if inspect.ismodule(member[1]) and os.path.isfile(inspect.getfile(member[1])):
                        # Create object for plugin and Set type
                        plugin = Plugin(self.__plugins_dir_path, member[0], plugin_type=subpackage)

                        # Add to package plugins
                        plugins[subpackage].append(plugin)
                self.logger.debug("Got the following '%s' plugins: %s" % (subpackage, plugins[subpackage]))

        self.__plugins = plugins

        self.logger.debug("EXIT")
        return plugins


    def __is_valid_plugin_name(self, name):
        '''
        Validates the specified plugin name

        :param name: The name to check
        :return: True if name is valid, otherwise False
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("Checking names '%s'" % name)

        if (
                (not self.PLUGIN_NAME_REGEX.match(name)) or
                (len(name) < self.PLUGIN_NAME_MIN_LEN) or
                (len(name) > self.PLUGIN_NAME_MAX_LEN)
        ):
            self.logger.debug("EXIT with False")
            return False
        else:
            self.logger.debug("EXIT with True")
            return True


    def __is_valid_plugin_type(self, plugin_type):
        '''
        Validates the plugin type

        :param plugin_type: plugin type
        :return: True if valid, else False
        '''
        self.logger.debug("ENTRY")
        self.logger.debug("Checking plugin type %s" % plugin_type)

        if plugin_type.lower() == "core" or plugin_type.lower() == "addon":
            self.logger.debug("EXIT with True")
            return True
        else:
            self.logger.debug("EXIT with False")
            return False
