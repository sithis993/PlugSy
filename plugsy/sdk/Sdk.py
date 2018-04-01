'''
Plugsy - Software Development Kit
'''

# Import libs
import os
import shutil
from .NewPlugin import NewPlugin
from .Exceptions import *
from ..Exceptions import *

class Sdk():
    '''
    SDK Class
    '''

    def __init__(self, plugins_home_path):
        '''
        Constructor
        @param plugins_home_path: The path of the plugins package directory
        '''
        # Check plugins home exists
        if not os.path.isdir(plugins_home_path):
            raise PluginsHomeNotFound(plugins_home_path)

        self.__plugins_dir_path = plugins_home_path


    def create_plugin(self, is_core_plugin, name, description=None, version=None, author=None, dependencies=[]):
        '''
        Creates a new plugin
        :return:
        '''

        if self.does_plugin_exist(name):
            raise PluginAlreadyExists(name)

        new_plugin = Plugin(
            is_core_plugin, name,
            self.__plugins_dir_path,
            description, version,
            author, dependencies
        )

        # Add new plugin package to subpackage (core, addon) __init__
        self.__add_plugin_to_init(new_plugin)


    def __add_plugin_to_init(self, new_plugin):
        '''
        Adds the new plugin import to the relevant subpackage
        @return:
        '''
        init_contents = ""
        subpackage_init_path = os.path.join(
            self.__plugins_dir_path,
            "core" if new_plugin.is_core_plugin() else "addon",
            "__init__.py"
        )

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
            print("Writing %s" % subpackage_init_path)
            init_file.write(init_contents)


    def __remove_plugin_from_init(self, name, is_core_plugin):
        '''
        Removes the Plugin package import from the subpackage __init__
        @param name: The name of the plugin to remove
        @param is_core_plugin: Whether the plugin is a core plugin
        @return:
        '''
        subpackage_init_path = os.path.join(
            self.__plugins_dir_path,
            "core" if is_core_plugin else "addon",
            "__init__.py"
        )

        if os.path.isfile(subpackage_init_path):
            # Read subpackage init
            print("Removing plugin from init")
            with open(subpackage_init_path, "r") as init_file:
                init_contents = init_file.read()

            # Remove import
            init_contents.replace("from . import %s" % name)

            # Write subpackage init
            with open(subpackage_init_path, "w") as init_file:
                init_file.write(init_contents)


    def does_plugin_exist(self, name):
        '''
        Checks if a plugin with the specified name already exists
        @param name: The name of the plugin to check for
        @return: plugin home path if the plugin exists, otherwise False
        @todo: Add more complete checking here (try import)
        '''
        core_plugin_path = os.path.join(self.__plugins_dir_path, "core", name)
        addon_plugin_path = os.path.join(self.__plugins_dir_path, "addon", name)
        plugin_class_path = os.path.join(self.__plugins_dir_path, "")

        if os.path.isdir(addon_plugin_path):
            if os.path.isfile(os.path.join(addon_plugin_path, "%s.py" % name)):
                return os.path.join(addon_plugin_path)
        if os.path.isdir(core_plugin_path):
            if os.path.isfile(os.path.join(core_plugin_path, "%s.py" % name)):
                return os.path.join(core_plugin_path)
        else:
            return False


    def delete_plugin(self, name):
        '''
        Deletes an existing plugin
        @param name: The name of the plugin to delete
        '''

        plugin_dir = self.does_plugin_exist(name)
        if not plugin_dir:
            raise PluginDoesNotExist(name)

        shutil.rmtree(plugin_dir)

        # Remove from init

