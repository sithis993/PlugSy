'''
Plugsy - Plugin Manager
'''

# Import standard libs
import importlib
import pkgutil
import sys
import time
import inspect
from toposort import toposort, CircularDependencyError

# Import project libs
from .Exceptions import *

####################################
# PlugSy Plugin Manager
####################################
class Plugsy():

    ROOT_PLUGIN_PACKAGE = "plugins"
    ADDON_DIR = "addon"
    CORE_DIR = "core"

    def __init__(self, safe_mode=False):
        '''
        Constructor
        @param: safe_mode: Boolean specifying whether Plugsy should be run in safe mode. In safe mode, only the
        core plugins will be loaded
        '''
        self.__plugins = []
        self.__safe_mode = safe_mode


    def activate_plugins(self, plugin_names=[], ignore_addon_dep_failures=False):
        '''
        @summary: Activates Plugsy plugins
        @param plugin_names: Optional list of specific plugins to activate
        @param ignore_addon_dep_failures: Boolean specifying whether dependency failures should be ignored
        or raised when loading Addon plugins
        '''
        loaded_plugins = []

        # Check for plugins package
        try:
            import plugins
        except ModuleNotFoundError:
            print("Error: Plugins directory not found. There are no plugins to activate")
            return

        # CORE - Start
        # --------------------------------------
        # Load core plugins
        core_plugins = self.__sort_by_dependencies(
            self.__load_plugins(
                subpackage=".".join([self.ROOT_PLUGIN_PACKAGE, self.CORE_DIR]),
                plugin_names=plugin_names
            ),
            False,
            loaded_plugins
        )

        if core_plugins:
            print("Core plugins loaded successfully")
        else:
            print("No core plugins were found")

        # Activate core plugins
        for plugin in core_plugins:
            plugin.activate()
        loaded_plugins += core_plugins
        # CORE - End
        # --------------------------------------

        # ADDON - Start
        # --------------------------------------
        # Load and activate addon plugins
        addon_plugins = self.__sort_by_dependencies(
            self.__load_plugins(
                subpackage=".".join([self.ROOT_PLUGIN_PACKAGE, self.ADDON_DIR]),
                plugin_names=plugin_names
            ),
            ignore_addon_dep_failures,
            loaded_plugins
        )

        if addon_plugins:
            print("Addon plugins loaded successfully")
        else:
            print("No addon plugins were found")

        # Activate addon plugins
        for plugin in addon_plugins:
            plugin.activate()
        loaded_plugins += addon_plugins
        # ADDON - End
        # --------------------------------------

        self.__set_plugins(loaded_plugins)
        time.sleep(2)
        print("-" * 50)


    def deactivate_plugins(self, plugin_names=[]):
        '''
        @summary: Deactivates all plugins, or a specific plugin
        '''

        # Deactivate specified plugin
        if plugin_names:
            for plugin_name in plugin_names:
                plugin = self.get_plugin(plugin_name)
                if plugin and plugin.is_activated():

                    # Make sure there isn't a dependent running
                    for active_plugin in self.get_plugins():
                        if plugin.get_name() in active_plugin.get_dependencies():
                            raise DependentRunning(plugin, active_plugin)
                        if plugin.is_core_plugin() and not active_plugin.is_core_plugin():
                            raise AddonPluginsStillRunning(plugin)

                    # Deactive and remove plugin
                    print("SHUTTING DOWN: %s" % plugin_name)
                    plugin.deactivate()
                    self.__plugins.remove(plugin)

        # Deactivate all plugins
        else:
            for plugin in self.get_plugins():
                if plugin.is_activated():
                    print("SHUTTING DOWN: %s" % plugin.get_name())
                    plugin.deactivate()
                    self.__plugins.remove(plugin)


    def __load_plugins(self, subpackage, plugin_names=[]):
        '''
        @summary: Loads Plugsy plugins
        @param subpackage: The subpackage to be loaded, such as 'core' or 'addons'
        @param plugin_names: An optional list of specific plugins to load
        @return: List of plugin objects
        '''
        plugins = []

        # Iterate packages and contained plugins
        for plugin in self.__import_available_plugins(subpackage):

            # Skip plugin load if name specified and not matching plugin, or plugin already loaded
            if (not plugin_names or plugin[0] in plugin_names) and not self.get_plugin(plugin[0]):
                try:
                    name, _class, plugin, configuration = self.__instantiate_plugin(plugin)
                    # Try to load the plugins
                    try:
                        if subpackage.lower().split(".")[0] == "core":
                            plugin.set_core_plugin()
                        plugin.load_configuration(configuration)
                    except Exception as nx:
                        raise InvalidPlugin(
                            plugin_name=name,
                            message=nx
                        )
                    plugins.append(plugin)
                except InvalidPlugin as ix:
                    # raise exception as "not a plugin or something"
                    if subpackage.lower().split(".")[0] == "core":
                        raise(ix)
                    else:
                        print("Skipping addon plugin '%s' due to error: %s" % (
                            ix.plugin_name,
                            ix.message
                            )
                        )

        return plugins


    def __import_available_plugins(self, package_name):
        '''
        Returns a list of tuples representing available plugins for the specified package
        @param: package_name: The name of the package to load plugins from, such as "core"
        @return: List of tuples containing (<plugin_name>, <plugin_module_reference>)
        '''
        available_plugins = []
        print("Importing plugins from package %s" % package_name)

        # Try to import parent_package
        try:
            package_import = importlib.import_module(package_name)
        except Exception:
            return available_plugins

        for member in inspect.getmembers(package_import):
            if inspect.ismodule(member[1]):
                plugin_location = ".".join([package_name, member[0]])
                available_plugins.append([
                    member[0], importlib.import_module(plugin_location)
                ])

        return available_plugins


    def __instantiate_plugin(self, plugin_package):
        '''
        Initiates an individual plugin and returns its class name and an instance
        @param plugin_package: Namespace location of the plugin package to initiate, such as plugin.core.api
        @return: The name of the plugins's class, a class reference, an instance of the object and it's config
        '''

        plugin_name = plugin_package[0]
        module_reference = plugin_package[1]

        try:
            plugin_class = getattr(module_reference, plugin_name)
            plugin_configuration = getattr(module_reference, "Config")
            plugin_object = plugin_class(
                plugsy=self
            )

            # Check plugin is valid
            try:
                if not plugin_object.is_initialised():
                    raise InvalidPlugin(plugin_name, "Plugin Not correctly initialised. super() must first be called")
            except AttributeError:
                raise InvalidPlugin(plugin_name, "Not an instance of AbstractPlugin")

            plugin_name = plugin_object.get_name()
        except (TypeError, AttributeError) as ex:
            raise InvalidPlugin(plugin_name, ex)

        return plugin_name, plugin_class, plugin_object, plugin_configuration


    def __sort_by_dependencies(self, plugins, ignore_dependency_failures, loaded_plugins):
        '''
        @summary: Sorts plugins by dependencies
        @param plugins: The plugin objects to sort
        @param ignore_dependency_failures: Boolean specifying with dependency failures should be suppressed
        @param loaded_plugins: List of plugins that have been loaded so far
        @return: Plugin objects in a sorted list
        @raise: PluginCircularDependency
        '''
        sorted_plugins = []
        dependency_dict = {}
        plugin_names = [plugin.get_name() for plugin in plugins]
        loaded_plugin_names = [loaded_plugin.get_name() for loaded_plugin in loaded_plugins]

        # If no plugins to sort, return empty list
        if not plugins:
            return list()

        # Determine sort type
        if plugins[0].is_core_plugin():
            core_sort = True
        else:
            core_sort = False

        # Check for unresolveable/missing dependencies
        for plugin in plugins:
            dependency_failure = False

            # If no dependencies, add to list and skip
            if not plugin.get_dependencies():
                sorted_plugins.append(plugin)
                continue

            # Check each dep is in the list of plugins to be loaded, or is already loaded or activated
            for dependency in plugin.get_dependencies():
                if dependency and dependency not in plugin_names and dependency not in loaded_plugin_names and not self.get_plugin(dependency):
                    if core_sort or (not core_sort and not ignore_dependency_failures):
                        raise MissingDependencyError(plugin, dependency)
                    elif not core_sort:
                        print("Error: Skipping Addon plugin '%s' due to unresolvable/missing dependency '%s'" % (plugin.get_name(), dependency))
                        dependency_failure = True

            # If dependency resolve failed and not fatal, skip plugin
            if dependency_failure:
                continue
            else:
                # Otherwise add plugins dependencies to dependency dict
                dependency_dict[plugin.get_name()] = plugin.get_dependencies()

        # Perform Topological Sort
        try:
            for dependency_set in toposort(dependency_dict):
                for dependency in dependency_set:
                    for plugin in plugins:
                        if plugin.get_name() == dependency:
                            sorted_plugins.append(plugin)
        except CircularDependencyError as cx:
            if core_sort or (not core_sort and not ignore_dependency_failures):
                raise PluginCircularDependency()
            else:
                print("Skipping Addon plugins due to Circular Dependency error")

        return sorted_plugins


    # =======================
    # = GETTERS
    # =======================
    def is_safe_mode_enabled(self):
        '''
        Return the boolean value of __safe_mode
        @return:
        '''

        return self.__safe_mode


    def get_plugin(self, plugin_name):
        '''
        Fetch the plugin object of a specific plugin
        @param plugin_name: The name of the plugin to fet
        @return: The relevant plugin object
        '''

        plugin_object = self.get_plugins(plugin_name=plugin_name)

        if not plugin_object:
            return None
        else:
            return plugin_object[0]


    def get_plugins(self, plugin_name=None):
        '''
        Fetches PlugSy plugins
        @param plugin_name: The name of a specific plugin to get (optional)
        :return: A list of PlugSy plugin objects
        '''
        plugins_list = []

        for plugin in self.__plugins:
            if not plugin_name or plugin.get_name() == plugin_name:
                plugins_list.append(plugin)

        return plugins_list


    def __get_plugin_subpackages(self):
        '''
        @summary: imports the plugins repository and returns the available subpackages
        @return: List of subpackages
        '''
        subpackages = []

        root_package_import = importlib.import_module(self.ROOT_PLUGIN_PACKAGE)
        for loader, modname, ispkg in pkgutil.iter_modules(root_package_import.__path__):
            if ispkg:
                subpackages.append(modname)

        return subpackages


    def __is_frozen(self):
        '''
        Checks if plugsy is running in a frozen context
        @return: True if frozen, otherwise False
        '''

        if hasattr(sys, 'frozen'):
            return True
        else:
            return False


    # =======================
    # = SETTERS
    # =======================
    def __set_plugins(self, plugins):
        '''
        Sets PlugSy's plugins
        @param plugins: A list of plugin objects
        '''

        self.__plugins += plugins

