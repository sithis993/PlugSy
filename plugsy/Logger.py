'''
Logger Class. Provides global logger access and handles initiation
'''

# import libs
import logging
import os

# import package content
from . import Config

class Logger():
    '''
    Provides a Logger object
    '''

    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s(): %(message)s"
    DEFAULT_LEVEL = logging.WARNING
    FILTERS_FILENAME = "debugfilters.conf"

    def __init__(self, name, level="", log_path=""):
        '''
        Constructor

        :param name: Debug name
        :param level: Logging level,
        :param log_path: Log file path
        '''

        # Init logger
        self.logger = logging.getLogger(name)

        # Configure logger if not already set up
        if not self.logger.hasHandlers():

            self.__formatter = logging.Formatter(self.LOG_FORMAT)
            self.__level = self.__get_level(level)
            self.logger.setLevel(self.__level)

            # Load filters and create filter object
            self.__filter = Filter(self.__get_filter_strings())

            # Configure handlers
            # Console
            self.__console = logging.StreamHandler()
            self.__console.setFormatter(self.__formatter)
            self.__console.addFilter(self.__filter)
            self.logger.addHandler(self.__console)
            # File
            if log_path:
                self.__file = logging.FileHandler(log_path, mode="w")
                self.__file.setFormatter(self.__formatter)
                self.__file.addFilter(self.__filter)
                self.logger.addHandler(self.__file)

            self.info("LOGGER INITIALISED")
            self.info("Level - '%s'" % logging.getLevelName(self.__level))
            self.info("%s - %s" % (Config.FULL_NAME, Config.VERSION))

            # Debug warning
            if logging.getLevelName(self.__level).lower() == "debug":
                self.warning("Debug level set to '%s'. This may hinder performance" % logging.getLevelName(self.__level))


    def __get_filter_strings(self):
        '''
        Loads and returns a list of debug filter strings

        :return: List of debug filter strings
        '''

        filters = Config.DEBUG_FILTERS
        filters_filepath = os.path.join(os.getcwd(), self.FILTERS_FILENAME)

        # Load any additional filters form filters file
        if os.path.isfile(filters_filepath):
            with open(filters_filepath, "r") as filter_file:
                for filter_string in filter_file.readlines():
                    if not filter_string.startswith("#"):
                        filters.append(filter_string.lower().rstrip())

        return filters



    ####################
    ## LOGGER METHODS ##
    ####################

    def debug(self, msg):
        '''
        Logs a DEBUG level entry

        :param msg: Message to log
        '''
        self.logger.debug(msg)


    def info(self, msg):
        '''
        Logs an INFO level entry

        :param msg: Message to log
        '''
        self.logger.info(msg)


    def warning(self, msg):
        '''
        Logs a WARNING level entry

        :param msg: Message to log
        '''
        self.logger.warning(msg)


    def error(self, msg):
        '''
        Logs an ERROR level entry

        :param msg: Message to log
        '''
        self.logger.error(msg)


    def critical(self, msg):
        '''
        Logs a CRITICAL level entry

        :param msg: Message to log
        '''
        self.logger.critical(msg)


    #############
    ## GETTERS ##
    #############

    def __get_level(self, level):
        '''
        Parses the level string and returns the matching logging integer

        :param level:
        '''
        logging_lvl = str(level)

        if level.lower() == "debug":
            logging_lvl = logging.DEBUG
        elif level.lower() == "info":
            logging_lvl = logging.INFO
        elif level.lower() == "error":
            logging_lvl = logging.ERROR
        else:
            logging_lvl = self.DEFAULT_LEVEL

        return logging_lvl


# ==========================
# = Filter Class
# ==========================
class Filter(logging.Filter):
    '''
    Custom filter for filtering to only specific sources, such as core plugins, addon plugins,
    or a simple specific plugin
    '''


    def __init__(self, filters):
        '''
        Constructor override

        :param filters: A list of filter names
        '''
        self.__filters = filters

        logging.Filter.__init__(self, name="")


    def filter(self, record):
        '''
        Custom filter method

        :param record: Debug record object
        :return: True if event is going to be logged. Otherwise False. Defaults to True if no filters found
        '''

        # If no filters, return True
        if not self.__filters:
            return True

        # Check for matching filter
        for filter in self.__filters:
            if record.name.lower().startswith(filter.lower()):
                return True

        return False
