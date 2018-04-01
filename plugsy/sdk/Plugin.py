'''
Plugsy SDK - Plugin Class - Holds methods for creating, deleting and editing a plugiin
'''

# Import libs
import os
from .Exceptions import *

class Plugin():
    '''
    Represent a plugin object
    '''

    TEMPLATE_PLUGIN_NAME = "PluginTemplate"

    def __init__(self, is_core_plugin, name, plugins_dir_path, description, version, author, dependencies=[]):
        '''
        Constructior
        '''
        self.__plugins_dir_path = plugins_dir_path
        self.__name = name

        # Set home
        if self.__is_core_plugin:
            self.__home = os.path.join(plugins_dir_path, "core", self.__name)
        else:
            self.__home = os.path.join(plugins_dir_path, "addons", self.__name)


    def create(self):
        '''
        Creates the plugin
        @return:
        '''

        # Create home
        try:
            os.makedirs(self.__home)
        except FileExistsError:
            raise PluginCreationFailure(self.__name, "The directory at '%s' already exists" % self.__home)

        # Add plugin package files
        self.__create_init()
        self.__create_config()
        self.__create_class_file()


    def __create_init(self):
        '''
        Creates the Plugin __init__.py
        @return:
        '''
        template_path = os.path.join(os.path.dirname(__file__), self.TEMPLATE_PLUGIN_NAME, "__init__.py")

        # Read init
        with open(template_path, "r") as template:
            new_init_contents = template.read().replace(self.TEMPLATE_PLUGIN_NAME, self.__name)

        # Write init
        with open(os.path.join(self.__home, "__init__.py"), "w") as new_init_file:
            new_init_file.write(new_init_contents)


    def __create_config(self):
        '''
        Create the plugins Config.py
        @return:
        '''
        template_path = os.path.join(os.path.dirname(__file__), self.TEMPLATE_PLUGIN_NAME, "Config.py")

        # Read config
        with open(template_path, "r") as template:
            new_config_contents = template.read().replace(self.TEMPLATE_PLUGIN_NAME, self.__name)

        # Write config
        with open(os.path.join(self.__home, "Config.py"), "w") as new_config_file:
            new_config_file.write(new_config_contents)


    def __create_class_file(self):
        '''
        Creates the main class file of the Plugin
        @return:
        '''
        template_path = os.path.join(os.path.dirname(__file__), self.TEMPLATE_PLUGIN_NAME, "%s.py" % self.TEMPLATE_PLUGIN_NAME)

        # Read plugin class
        with open(template_path, "r") as template:
            new_class_contents = template.read().replace(self.TEMPLATE_PLUGIN_NAME, self.__name)

        # Write plugin class
        with open(os.path.join(self.__home, "%s.py" % self.__name), "w") as new_class_file:
            new_class_file.write(new_class_contents)


    #############
    ## GETTERS ##
    #############
    def get_name(self):
        '''
        Get's plugin name
        @return: Plugin name
        '''
        return self.__name

    def get_description(self):
        '''
        Get's plugin description
        @return: Plugin description
        '''
        return self.__description

    def get_version(self):
        '''
        Get's plugin version
        @return: Plugin version
        '''
        return self.__version

    def get_author(self):
        '''
        Get's plugin author
        @return: Plugin author
        '''
        return self.__author

    def get_dependencies(self):
        '''
        Get's plugin dependencies
        @return: Plugin dependencies
        '''
        return self.__dependencies


    def get_home(self):
        '''
        Gets the plugin's home dir path
        @return: Home dir
        '''
        return self.__home

    def is_core_plugin(self):
        '''
        Get's plugin core status
        @return: True or False
        '''

        return self.__is_core_plugin


    #############
    ## SETTERS ##
    #############
    def set_core_plugin(self, core):
        '''
        For setting the plugin as core or not core
        @param core: True of False
        @return:
        '''



