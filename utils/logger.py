import logging

from config.common import LOG_FILEPATH

# set logger and format
logger = logging.getLogger()
logFormat = logging.Formatter("[%(asctime)s - %(name)s]: %(levelname)s - %(message)s (%(funcName)s - line %(lineno)d)",
                              datefmt='%H:%M:%S')

# set level of logging
logger.setLevel(logging.INFO)

# file settings
fileHandler = logging.FileHandler(LOG_FILEPATH)
fileHandler.setFormatter(logFormat)
logger.addHandler(fileHandler)
