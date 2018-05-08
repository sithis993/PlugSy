'''
Plugsy - Logger Class. Provides global logger access and handles initiation
'''

# import libs
import logging

# import package content

class Logger():
    '''
    Provides a Logger object
    '''

    LOG_FORMAT = "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
    DEFAULT_LEVEL = logging.WARNING

    def __init__(self, name, level="", log_path=""):
        '''
        Constructor
        @param level: Logging level,
        @param log_path: Log file path
        @todo: Add filtering to only show debug of certain objects (None by default)
        '''

        # Init logger
        self.__logger = logging.getLogger(name)

        # Configure logger if not already set up
        if not self.__logger.hasHandlers():
            self.__formatter = logging.Formatter(self.LOG_FORMAT)
            self.__level = self.__get_level(level)
            self.__logger.setLevel(self.__level)

            # Configure handlers
            # Console
            self.__console = logging.StreamHandler()
            self.__console.setFormatter(self.__formatter)
            self.__logger.addHandler(self.__console)
            # File
            if log_path:
                self.__file = logging.FileHandler(log_path, mode="w")
                self.__file.setFormatter(self.__formatter)
                self.__logger.addHandler(self.__file)



    ####################
    ## LOGGER METHODS ##
    ####################

    def debug(self, msg):
        '''
        Logs a DEBUG level entry
        @param msg: Message to log
        @return:
        '''
        self.__logger.debug(msg)


    def info(self, msg):
        '''
        Logs an INFO level entry
        @param msg: Message to log
        @return:
        '''
        self.__logger.info(msg)


    def warning(self, msg):
        '''
        Logs a WARNING level entry
        @param msg: Message to log
        @return:
        '''
        self.__logger.warning(msg)


    def error(self, msg):
        '''
        Logs an ERROR level entry
        @param msg: Message to log
        @return:
        '''
        self.__logger.error(msg)


    def critical(self, msg):
        '''
        Logs a CRITICAL level entry
        @param msg: Message to log
        @return:
        '''
        self.__logger.critical(msg)


    #############
    ## GETTERS ##
    #############

    def __get_level(self, level):
        '''
        Parses the level string and returns the matching logging integer
        @param level:
        @return:
        '''

        if level.lower() == "debug":
            logging_lvl = logging.DEBUG
        elif level.lower() == "info":
            logging_lvl = logging.INFO
        elif level.lower() == "error":
            logging_lvl = logging.ERROR
        else:
            logging_lvl = self.DEFAULT_LEVEL

        return logging_lvl

