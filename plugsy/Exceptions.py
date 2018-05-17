'''
@summary: Plugsy - Exceptions
:@author: MLS
'''


#################################################
# InvalidPlugin
#################################################
class InvalidPlugin(Exception):
    '''
    @summary: To be raised when trying to import a broken/invalid Plugsy plugin
    '''

    def __init__(self, plugin_name, message):
        '''
        Constructor
        @param plugin_name: The name of the plugin at fault
        @param message: Exception message
        '''
        self.message = "Could not load plugin: {}. Check that the plugin is a valid instance of AbstractPlugin"\
            " and that super() is called".format(message)
        self.plugin_name = plugin_name

        super(InvalidPlugin, self).__init__(message)


    def __str__(self):
        return self.message

#################################################
# InvalidDependency
#################################################
class InvalidDependency(Exception):
    '''
    @summary: To be raised in the event of an invalid plugin dependency, such as
    a core plugin depending on an addon plugin
    '''

    def __init__(self, message):
        '''
        Constructor
        @param message: Exception message
        '''
        self.message = message
        super(InvalidDependency, self).__init__(message)


    def __str__(self):
        return self.message


#################################################
# CorePluginCircularDependency
#################################################
class CorePluginCircularDependency(Exception):
    '''
    @summary: To be raised in the event of a Core plugin Circular Dependency
    '''

    def __init__(self, message):
        '''
        Constructor
        @param message: Exception message
        '''
        self.message = message
        super(CorePluginCircularDependency, self).__init__(message)


    def __str__(self):
        return self.message

#################################################
# AddonPluginCircularDependency
#################################################
class AddonPluginCircularDependency(Exception):
    '''
    @summary: To be raised in the event of an Addon plugin Circular Dependency
    '''

    def __init__(self, message):
        '''
        Constructor
        @param message: Exception message
        '''
        self.message = message
        super(AddonPluginCircularDependency, self).__init__(message)


    def __str__(self):
        return self.message


#################################################
# Plugin Circular Dependency
#################################################
class PluginCircularDependency(Exception):
    '''
    @summary: To be raised in the event of plugin Circular Dependency
    '''

    def __init__(self):
        '''
        Constructor
        @param message: Exception message
        '''
        self.message = "Circular Dependency error encountered whilst loading plugins"
        super(PluginCircularDependency, self).__init__(self.message)


    def __str__(self):
        return self.message


#################################################
# MissingDependencyError
#################################################
class MissingDependencyError(Exception):
    '''
    @summary: To be raised in the event of a missing plugin dependency
    '''

    def __init__(self, plugin, dependency):
        '''
        Constructor
        @param plugin: Plugin object
        @param dependency: Plugin object's failed dependency
        '''
        if plugin.is_core_plugin():
            message = "Core plugin '%s' has missing or unresolvable dependency '%s'" % (
                plugin.get_name(),
                dependency
            )
        else:
            message = "Addon plugin '%s' has missing or unresolvable dependency '%s'" % (
                plugin.get_name(),
                dependency
            )
        self.message = message
        super(MissingDependencyError, self).__init__(message)


    def __str__(self):
        return self.message

#################################################
# DependentRunning
#################################################
class DependentRunning(Exception):
    '''
    @summary: To be raised if a plugin is being deactivated, but there are other plugins running
    which depend upon this plugin
    '''

    def __init__(self, plugin, dependent):
        '''
        Constructor
        @param plugin: The Plugin object being deactivated
        @param dependent: The dependent plugin object
        '''
        self.message = "plugin '%s' is depended upon by plugin '%s' and could not be deactivated" % (
            plugin.get_name(),
            dependent.get_name()
        )
        super(DependentRunning, self).__init__(self.message)


    def __str__(self):
        return self.message


#################################################
# AddonPluginsStillRunning
#################################################
class AddonPluginsStillRunning(Exception):
    '''
    @summary: To be raised if trying to deactive a core plugin but there are still add on plugins running
    '''

    def __init__(self, plugin):
        '''
        Constructor
        @param plugin: The Plugin object being deactivated
        '''
        self.message = "Cannot deactivate core plugin '%s' whilst addon plugins are still running" % plugin.get_name()
        super(AddonPluginsStillRunning, self).__init__(self.message)


    def __str__(self):
        return self.message


#################################################
# PluginDoesNotExist
#################################################
class PluginDoesNotExist(Exception):
    '''
    To be raised if a plugin does not exist
    '''

    def __init__(self, name):
        '''
        Constructor
        @param name: The name of the plugin
        '''
        message = "The plugin '%s' does not exist" % name
        Exception.__init__(self, message)


#################################################
# SubpackageImportError
#################################################
class SubpackageImportError(Exception):
    '''
    To be raised in the event of a fatal subpackage import (core, addon)
    '''

    def __init__(self, subpackage, import_exception):
        '''
        Constructor
        @param subpackage: The name of the failed subpackage
        @param import_exception: The actual import exception
        '''
        message = "A fatal error occured whilst attempting to import the subpackage '%s': %s" % (
            subpackage, import_exception
        )
        Exception.__init__(self, message)


