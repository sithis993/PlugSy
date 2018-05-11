'''
@summary: Defines Abstract Plugin and Interface that all plugins must dervice from
@author: MLS
'''

# Import libs
from threading import Thread
from threading import Event

# Import package modules
from . import Config
from .Logger import Logger

class AbstractPlugin(Thread, Logger):

    def __init__(self, plugsy, name=None):
        '''
        Constructor
        @param plugsy: Parent PlugSy object
        @param name: The name of the plugin. Optional, overrides package name
        '''
        self.__activated = False
        self.__loaded = False
        self.__is_core_plugin = False
        self.__is_initialised = True
        self.plugsy = plugsy
        self.stop_event = Event()

        # Set name
        if not name:
            self.__set_name(self.__class__.__name__)
        else:
            self.__set_name(name)

        # Super
        Thread.__init__(self)


    def run(self):
        '''
        Plugin Main run method holding the core pugin code. Called upon plugin activation
        @note: Must be overriden by derived classes (plugins)
        @raise: NotImplementedError
        '''

        self.logger.error("Plugin does not have a run() method")
        raise NotImplementedError(
            "Abstract run() method must be implemented by '%s'" %
            self.__class__.__name__
        )


    def stop(self):
        '''
        Plugin stop method. Stops plugin execution by setting stop event to iterrupt actions
        '''
        self.logger.debug("ENTRY")

        self.stop_event.set()
        self.logger.debug("EXIT")


    def load_configuration(self, configuration):
        '''
        Loads the plugin configuration into the plugin object
        @param configuration: Plugin configuration module
        '''
        self.logger.debug("ENTRY")

        # Load plugin dependencies
        self.set_dependencies(configuration.DEPENDENCIES)
        self.logger.debug("EXIT")


    def activate(self):
        '''
        Activates the plugin and starts the thread
        '''
        self.logger.debug("ENTRY")
        self.__activated = True

        # Start main thread
        self.start()

        self.logger.info("Plugin activated!")
        self.logger.debug("EXIT")


    def deactivate(self):
        '''
        Deactivates the thread and calls the plugin stop method
        '''
        self.logger.debug("ENTRY")

        self.stop()

        # TODO Wait until we're no longer running before setting this and returning. Might need to close handles etc.
        self.__activated = True
        self.logger.info("Plugin deactivated!")
        self.logger.debug("EXIT")


    def init_logging(self):
        '''
        Initialises plugin logging
        @return:
        '''
        plugin_package = "core" if self.__is_core_plugin else "addon"

        # init logging
        Logger.__init__(
            self,
            name="%s.plugins.%s.%s" % (Config.FULL_NAME, plugin_package, self.__name)
        )


    # =======================
    # = GETTERS
    # =======================
    def is_activated(self):
        '''
        Checks whether the plugin has been activated
        @return: True if activated, otherwise False
        '''
        self.logger.debug("ENTRY")

        self.logger.debug("EXIT")
        return self.__activated

    def get_name(self):
        '''
        Gets the plugins name
        @return: Plugin name
        '''

        return self.__name


    def is_core_plugin(self):
        '''
        Checks whether the plugin is a core plugin (within the core subpackage)
        @return: True if plugin is a core plugin, otherwise False
        '''
        self.logger.debug("ENTRY")

        self.logger.debug("EXIT")
        return self.__is_core_plugin


    def is_initialised(self):
        '''
        Checks if the plugin has been initialised
        @return: True if initialised, otherwise False
        '''

        try:
            self.__is_initialised
            return True
        except AttributeError:
            return False


    def get_dependencies(self):
        '''
        Fetches the plugin's dependencies
        @return: Plugin dependencies as a list of strings (plugin names)
        '''
        self.logger.debug("ENTRY")

        self.logger.debug("EXIT")
        return self.__dependencies


    # =======================
    # = SETTERS
    # =======================
    def __set_name(self, name):
        '''
        Sets the plugins name
        @param name: The name of the plugin
        '''

        self.__name = name


    def set_dependencies(self, dependencies):
        '''
        Sets the plugin's dependencies
        @param dependencies: A list of plugins that the plugin depends on
        '''
        self.logger.debug("ENTRY")
        dependency_set = set()

        for dependency in dependencies:
            dependency_set.add(dependency.lower())

        self.__dependencies = dependency_set
        self.logger.debug("Plugin dependencies set to '%s'" % dependencies)
        self.logger.debug("EXIT")


    def set_core_plugin(self):
        '''
        sets the plugin as a core plugin when called
        '''

        self.__is_core_plugin = True



