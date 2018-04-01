'''
Plugsy - Software Development Kit
'''

# Import libs
import os
import re
from .Plugin import Plugin
from .Exceptions import *
from ..Exceptions import *

class Sdk():
    '''
    SDK Class
    '''

    PLUGIN_NAME_REGEX = re.compile("^[a-zA-Z]+[a-zA-Z0-9_]*$")
    PLUGIN_NAME_MIN_LEN = 3
    PLUGIN_NAME_MAX_LEN = 35

    def __init__(self, plugins_home_path):
        '''
        Constructor
        @param plugins_home_path: The path of the plugins package directory
        '''
        # Check plugins home exists
        if not os.path.isdir(plugins_home_path):
            raise PluginsHomeNotFound(plugins_home_path)

        self.__plugins_dir_path = plugins_home_path


    def create_plugin(self, plugin_type, name, description=None, version=None, author=None, dependencies=[]):
        '''
        Creates a new plugin
        :return:
        '''

        # Check name
        self.__validate_plugin_name(name)

        # Initiate plugin
        new_plugin = Plugin(
            plugins_dir_path=self.__plugins_dir_path, name=name
        )

        # Set type
        if plugin_type.lower() == "core":
            new_plugin.set_core_plugin(True)
        else:
            new_plugin.set_core_plugin(False)

        # Set any additional options
        # TODO Do this when at a good point and figure out where to add them
        #if description:
        #    new_plugin.set_description(description)
        #if version:

        # Create
        new_plugin.create()

        # Add new plugin package to subpackage (core, addon) __init__
        self.__add_plugin_to_init(new_plugin)


    def delete_plugin(self, name):
        '''
        Deletes an existing plugin
        @param name: The name of the plugin to delete
        '''

        # Initiate plugin and delete
        existing_plugin = Plugin(self.__plugins_dir_path, name)
        existing_plugin.delete()

        # Remove from init
        self.__remove_plugin_from_init(existing_plugin)


    def __validate_plugin_name(self, name):
        '''
        Validates the specified plugin name
        @param name: The name to check
        @raise BadPluginName: If invalid
        '''

        if (
                (not self.PLUGIN_NAME_REGEX.match(name)) or
                (len(name) < self.PLUGIN_NAME_MIN_LEN) or
                (len(name) > self.PLUGIN_NAME_MAX_LEN)
        ):
            raise BadPluginName(name)


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
            init_file.write(init_contents)


    def __remove_plugin_from_init(self, existing_plugin):
        '''
        Removes the Plugin package import from the subpackage __init__
        @param name: The name of the plugin to remove
        @return:
        '''
        subpackage_init_path = os.path.join(
            self.__plugins_dir_path,
            "core" if existing_plugin.is_core_plugin() else "addon",
            "__init__.py"
        )

        if os.path.isfile(subpackage_init_path):
            # Read subpackage init
            with open(subpackage_init_path, "r") as init_file:
                init_contents = init_file.read()

            # Remove import
            init_contents = init_contents.replace("from . import %s\n" % existing_plugin.get_name(), "")

            # Write subpackage init
            with open(subpackage_init_path, "w") as init_file:
                init_file.write(init_contents)

