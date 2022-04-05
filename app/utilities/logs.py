import logging as log

# Set logging configuration
log.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=log.DEBUG)

# Utility class for logging
class Log:
    @staticmethod
    def d(TAG, message): # Debug
        Log.__checkParameters(TAG, message)
        Log.__log(log.DEBUG, TAG, message)

    @staticmethod
    def i(TAG, message): # Info
        Log.__checkParameters(TAG, message)
        Log.__log(log.INFO, TAG, message)

    @staticmethod
    def w(TAG, message): # Warning
        Log.__checkParameters(TAG, message)
        Log.__log(log.WARNING, TAG, message)

    @staticmethod
    def e(TAG, message): # Error
        Log.__checkParameters(TAG, message)
        Log.__log(log.ERROR, TAG, message)

    @staticmethod
    def c(TAG, message): # Critical
        Log.__checkParameters(TAG, message)
        Log.__log(log.CRITICAL, TAG, message)

    @staticmethod
    def __log(level, TAG, message):
        Log.__checkParameters(TAG, message)
        log.log(level, TAG + ": " + message)

    @staticmethod
    def __checkParameters(TAG, message):
        if (TAG is None or message is None):
            raise Exception("Invalid parameters")