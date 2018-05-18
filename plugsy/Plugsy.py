'''
Plugsy - Plugin System
'''

# Import standard libs
import importlib
import pkgutil
import sys
import time
import inspect
from toposort import toposort, CircularDependencyError

# Import project libs
from . import Config
from .Logger import Logger
from .Exceptions import *

####################################
# PlugSy Plugin Manager
####################################
class Plugsy(Logger):

    ROOT_PLUGIN_PACKAGE = "plugins"
    ADDON_DIR = "addon"
    CORE_DIR = "core"

    def __init__(self, safe_mode=False, debug_level="", debug_log_path=""):
        '''
        Constructor

        :param safe_mode: Boolean specifying whether Plugsy should be run in safe mode. In safe mode, only the
            core plugins will be loaded
        :param debug_level: Level of debug. Should be one or INFO, DEBUG, WARNING or ERROR
        :param debug_log_path: Optional peth to a debug log file. WIll be created and used for logging if specified
        '''
        Logger.__init__(
            self,
            name=Config.FULL_NAME,
            level=debug_level, log_path=debug_log_path
        )
        self.__plugins = []
        self.__safe_mode = safe_mode


    def activate_plugins(self, plugin_names=[], ignore_addon_dep_failures=False):
        '''
        Activates Plugsy plugins

        :param plugin_names: Optional list of specific plugins to activate
        :param ignore_addon_dep_failures: Boolean specifying whether dependency failures should be ignored or raised
            when loading Addon plugins
        '''
        self.logger.debug("ENTRY")
        loaded_plugins = []
        self.logger.debug("Ignoring Addon dependency failures: %s" % ignore_addon_dep_failures)

        # Check plugin_names is correct type
        if not isinstance(plugin_names, list):
            self.logger.error(
                "Expected plugin_names arg to be list, but got %s" %
                type(plugin_names)
            )
            raise TypeError("plugin_names argument must be list")

        if plugin_names:
            self.logger.debug("plugin names specified. Trying to load '%s'")
        else:
            self.logger.debug("plugin names not specified. Activating all plugins")

        # Check for plugins package
        try:
            import plugins
            self.logger.debug("plugins directory imported successfully")
        except ImportError:
            self.logger.critical("Plugins directory not found. There are no plugins to activate")
            return

        # CORE - Start
        # --------------------------------------
        # Load core plugins
        self.logger.debug(" Loading core plugins")
        core_plugins = self.__sort_by_dependencies(
            self.__load_plugins(
                subpackage=".".join([self.ROOT_PLUGIN_PACKAGE, self.CORE_DIR]),
                plugin_names=[plugin_name.lower() for plugin_name in plugin_names]
            ),
            False,
            loaded_plugins
        )

        if core_plugins:
            self.logger.info("%s Core plugins imported successfully" % len(core_plugins))
        else:
            self.logger.info("No core plugins were found")

        # Activate core plugins
        self.logger.debug("Activating core plugins")
        for plugin in core_plugins:
            self.logger.debug(" Activating '%s'" % plugin.get_name())
            plugin.activate()
        loaded_plugins += core_plugins
        self.logger.debug("Finished loading core plugins")
        # CORE - End
        # --------------------------------------

        # ADDON - Start
        # --------------------------------------
        # Load and activate addon plugins
        self.logger.debug("Activating addon plugins")
        addon_plugins = self.__sort_by_dependencies(
            self.__load_plugins(
                subpackage=".".join([self.ROOT_PLUGIN_PACKAGE, self.ADDON_DIR]),
                plugin_names=[plugin_name.lower() for plugin_name in plugin_names]
            ),
            ignore_addon_dep_failures,
            loaded_plugins
        )

        if addon_plugins:
            self.logger.info("%s Addon plugins imported successfully" % len(addon_plugins))
        else:
            self.logger.info("No Addon plugins were found")

        # Activate addon plugins
        self.logger.debug("Activating addon plugins")
        for plugin in addon_plugins:
            self.logger.debug("Activating '%s'" % plugin.get_name())
            plugin.activate()
        loaded_plugins += addon_plugins
        self.logger.debug("Finished activating core plugins")
        # ADDON - End
        # --------------------------------------

        # Set Plugsy plugins
        self.__set_plugins(loaded_plugins)

        self.logger.debug("EXIT")


    def deactivate_plugins(self, plugin_names=[]):
        '''
        Deactivates all plugins, or a specific plugin

        :param plugin_names: Optional list of plugin names to deactivate
        '''
        self.logger.debug("ENTRY")

        # Check plugin_names is correct type
        if not isinstance(plugin_names, list):
            self.logger.error(
                "Expected plugin_names arg to be list, but got %s" %
                type(plugin_names)
            )
            raise TypeError("plugin_names argument must be list")

        # Deactivate specified plugin
        if plugin_names:
            self.logger.debug("plugin names specified. Deactivating '%s'" % plugin_names)
            for plugin_name in plugin_names:

                # Get object of Plugin
                plugin = self.get_plugin(plugin_name)
                if plugin and plugin.is_activated():
                    self.logger.debug("plugin '%s' exists and is active" % plugin.get_name())

                    # Make sure there isn't a dependent running
                    self.logger.debug("Checking for dependencies")
                    for active_plugin in self.get_plugins():

                        # Check if there's a plugin running that depends on the plugin being deactivated
                        if plugin.get_name() in active_plugin.get_dependencies():
                            self.logger.error(
                                "'%s' is depended upon by running plugin '%s',"
                                 "and cannot be deactivated" % (plugin_name, active_plugin.get_name())
                            )
                            raise DependentRunning(plugin, active_plugin)

                        # If the plugin is a core plugin, make sure there are no addon plugins still running
                        elif plugin.is_core_plugin() and not active_plugin.is_core_plugin():
                            self.logger.error(
                                "'%s' is a core plugin and there are still addon"
                                " plugins currently running" % plugin_name
                            )
                            raise AddonPluginsStillRunning(plugin)


                    # Deactive and remove plugin
                    self.logger.debug("shutting down plugin '%s' and removing from plugins array" % plugin_name)
                    plugin.deactivate()
                    self.__plugins.remove(plugin)

                else:
                    self.logger.error("No plugin object found for '%s', or plugin not active" %
                                      plugin_name
                                      )

        # Deactivate all plugins
        else:
            self.logger.debug("plugin names not specified. Deactivating all plugins")
            for plugin in self.get_plugins():
                if plugin.is_activated():
                    self.logger.debug("shutting down plugin '%s' and removing from plugins array" % plugin.get_name())
                    plugin.deactivate()
                    self.__plugins.remove(plugin)


        self.logger.debug("plugins array: %s" % self.__plugins)
        self.logger.debug("EXIT")


    def __load_plugins(self, subpackage, plugin_names=[]):
        '''
        Loads Plugsy plugins

        :param subpackage: The subpackage to be loaded, such as 'core' or 'addons'
        :param plugin_names: An optional list of specific plugins to load
        :return: List of plugin objects
        '''
        self.logger.debug("ENTRY")
        plugins = []

        # Iterate packages and contained plugins
        for plugin in self.__import_available_plugins(subpackage):

            # Skip plugin load if name specified and not matching plugin, or plugin already loaded
            if (not plugin_names or plugin[0].lower() in plugin_names) and not self.get_plugin(plugin[0]):
                self.logger.debug("Attempting to load '%s' plugin" % plugin[0])
                try:
                    name, _class, plugin, configuration = self.__instantiate_plugin(plugin)
                    self.logger.debug("'%s' loaded successfully" % name)
                    # Try to load the plugins
                    try:
                        if subpackage.lower().split(".")[1] == "core":
                            self.logger.debug("Setting plugin as core plugin")
                            plugin.set_core_plugin()
                        plugin.init_logging()
                        self.logger.debug("Loading plugin config")
                        plugin.load_configuration(configuration)
                    except Exception as nx:
                        raise InvalidPlugin(
                            plugin_name=name,
                            message=nx
                        )
                    plugins.append(plugin)
                except InvalidPlugin as ix:
                    # raise exception as "not a plugin or something"
                    if subpackage.lower().split(".")[1] == "core":
                        self.logger.critical("Could not import core plugin")
                        raise(ix)
                    else:
                        self.logger.error(
                            "Skipping plugin '%s' due to load error: %s" % (
                                ix.plugin_name,
                                ix.message
                            )
                        )

        self.logger.debug("EXIT")
        return plugins


    def __import_available_plugins(self, package_name):
        '''
        imports available plugins for the specified package

        :param package_name: The name of the package to load plugins from, such as "core"
        :return: List of tuples containing (<plugin_name>, <plugin_module_reference>)
        '''
        self.logger.debug("ENTRY")
        available_plugins = []
        self.logger.debug("Importing plugins from package %s" % package_name)

        # Try to import parent_package
        try:
            package_import = importlib.import_module(package_name)
            self.logger.debug("Subpackage '%s' successfully imported" % package_name)
        except Exception as ix:
            self.logger.error("Could not import subpackage '%s'" % package_name)
            if "core" in package_name.lower():
                raise SubpackageImportError(package_name, ix)
            return available_plugins

        for member in inspect.getmembers(package_import):
            if inspect.ismodule(member[1]):
                self.logger.debug("member '%s' is a module. Adding import to available plugins" % member[0])
                plugin_location = ".".join([package_name, member[0]])
                available_plugins.append([
                    member[0], importlib.import_module(plugin_location)
                ])

        self.logger.debug("EXIT")
        return available_plugins


    def __instantiate_plugin(self, plugin_package):
        '''
        Initiates an individual plugin and returns its class name and an instance

        :param plugin_package: Namespace location of the plugin package to initiate, such as plugin.core.api
        :return: The name of the plugins's class, a class reference, an instance of the object and it's config
        '''
        self.logger.debug("ENTRY")

        plugin_name = plugin_package[0]
        module_reference = plugin_package[1]
        self.logger.debug("Attempting instantiation of '%s' plugin" % plugin_name)

        try:
            plugin_class = getattr(module_reference, plugin_name)
            plugin_configuration = getattr(module_reference, "Config")
            plugin_object = plugin_class(
                plugsy=self
            )

            # Check plugin is valid
            try:
                if not plugin_object.is_initialised():
                    self.logger.error("Plugin not initialised")
                    raise InvalidPlugin(plugin_name, "Plugin Not correctly initialised. super() must first be called")
                else:
                    self.logger.debug("Plugin has been initialised")
            except AttributeError:
                self.logger.error("Plugin is invalid (not an instance of AbstractPlugin)")
                raise InvalidPlugin(plugin_name, "Not an instance of AbstractPlugin")

            plugin_name = plugin_object.get_name()
        except (TypeError, AttributeError) as ex:
            self.logger.error("Plugin is invalid (Bad type or initiation)")
            raise InvalidPlugin(plugin_name, ex)

        self.logger.debug("EXIT")
        return plugin_name, plugin_class, plugin_object, plugin_configuration


    def __sort_by_dependencies(self, plugins, ignore_dependency_failures, loaded_plugins):
        '''
        Sorts plugins by dependencies

        :param plugins: The plugin objects to sort
        :param ignore_dependency_failures: Boolean specifying with dependency failures should be suppressed
        :param loaded_plugins: List of plugins that have been loaded so far
        :return: Plugin objects in a sorted list
        :raise: PluginCircularDependency
        '''
        self.logger.debug("ENTRY")
        sorted_plugins = []
        dependency_dict = {}
        plugin_names = [plugin.get_name().lower() for plugin in plugins]
        loaded_plugin_names = [loaded_plugin.get_name().lower() for loaded_plugin in loaded_plugins]

        # If no plugins to sort, return empty list
        if not plugins:
            self.logger.debug("No plugin objects to sort")
            return list()

        # Determine sort type
        if plugins[0].is_core_plugin():
            self.logger.debug("Sorting core plugins")
            core_sort = True
        else:
            self.logger.debug("Sorting addon plugins")
            core_sort = False

        # Check for unresolveable/missing dependencies
        for plugin in plugins:
            dependency_failure = False

            # If no dependencies, add to list and skip
            if not plugin.get_dependencies():
                self.logger.debug("plugin '%s' has no dependencies. Skipping" % plugin.get_name())
                sorted_plugins.append(plugin)
                continue

            # Check each dep is in the list of plugins to be loaded, or is already loaded or activated
            for dependency in [dependency.lower() for dependency in plugin.get_dependencies()]:
                if dependency and dependency not in plugin_names and dependency not in loaded_plugin_names and not self.get_plugin(dependency):
                    if core_sort or (not core_sort and not ignore_dependency_failures):
                        self.logger.critical(
                            "core plugin '%s' has missing dependency '%s'" % (
                                plugin.get_name(), dependency
                            )
                        )
                        raise MissingDependencyError(plugin, dependency)
                    elif not core_sort:
                        self.logger.error(
                            "Skipping addon plugin '%s' due to missing dependency" % (
                                plugin.get_name(), dependency
                            )
                        )
                        dependency_failure = True

            # If dependency resolve failed and not fatal, skip plugin
            if dependency_failure:
                continue
            else:
                # Otherwise add plugins dependencies to dependency dict
                dependency_dict[plugin.get_name().lower()] = plugin.get_dependencies()

        # Perform Topological Sort
        self.logger.debug("Performing topological sort: %s" % dependency_dict)
        try:
            for dependency_set in toposort(dependency_dict):
                for dependency in dependency_set:
                    for plugin in plugins:
                        if plugin.get_name().lower() == dependency and plugin not in sorted_plugins:
                            sorted_plugins.append(plugin)
        except CircularDependencyError as cx:
            if core_sort or (not core_sort and not ignore_dependency_failures):
                self.logger.critical(
                    "encountered fatal circular dependency error while loading plugins"
                )
                raise PluginCircularDependency()
            else:
                self.logger.error("Skipping addon plugins due to circular dependency error")

        self.logger.debug("EXIT with %s" % sorted_plugins)
        return sorted_plugins


    # =======================
    # = GETTERS
    # =======================
    def is_safe_mode_enabled(self):
        '''
        Return the boolean value of __safe_mode

        :return: True or False
        '''
        self.logger.debug("ENTRY")

        self.logger.debug("EXIT: %s" % self.__safe_mode)
        return self.__safe_mode


    def get_plugin(self, plugin_name):
        '''
        Fetch the plugin object of a specific plugin

        :param plugin_name: The name of the plugin to fetch
        :return: The relevant plugin object
        '''
        self.logger.debug("ENTRY")

        plugin_object = self.get_plugins(plugin_name=plugin_name)

        if not plugin_object:
            self.logger.debug("Plugin object does not exist")
            self.logger.debug("EXIT")
            return None
        else:
            self.logger.debug("Plugin object does exist")
            self.logger.debug("EXIT")
            return plugin_object[0]


    def get_plugins(self, plugin_name=None):
        '''
        Fetches PlugSy plugins

        :param plugin_name: The name of a specific plugin to get (optional)
        :return: A list of PlugSy plugin objects
        '''
        self.logger.debug("ENTRY")
        plugins_list = []

        for plugin in self.__plugins:
            if not plugin_name or plugin.get_name().lower() == plugin_name.lower():
                self.logger.debug("Got plugin '%s'" % plugin.get_name())
                plugins_list.append(plugin)

        self.logger.debug("EXIT")
        return plugins_list


    def __get_plugin_subpackages(self):
        '''
        :summary: imports the plugins repository and returns the available subpackages

        :return: List of subpackages
        '''
        self.logger.debug("ENTRY")
        subpackages = []

        root_package_import = importlib.import_module(self.ROOT_PLUGIN_PACKAGE)
        for loader, modname, ispkg in pkgutil.iter_modules(root_package_import.__path__):
            if ispkg:
                self.logger.debug("ENTRY")
                subpackages.append(modname)

        self.logger.debug("EXIT")
        return subpackages


    def __is_frozen(self):
        '''
        Checks if plugsy is running in a frozen context

        :return: True if frozen, otherwise False
        '''
        self.logger.debug("ENTRY")

        if hasattr(sys, 'frozen'):
            self.logger.debug("EXIT with %s" % True)
            return True
        else:
            self.logger.debug("EXIT with %s" % False)
            return False


    # =======================
    # = SETTERS
    # =======================
    def __set_plugins(self, plugins):
        '''
        Sets PlugSy's plugins

        :param plugins: A list of plugin objects
        '''
        self.logger.debug("ENTRY")

        self.__plugins += plugins
        self.logger.debug("EXIT")

