import os
from datetime import date
import logging


class logger():

    def __init__(self, tag=None):
        """
        Initialization of the logger
        """
        self.log_file = date.today().isoformat() + '.log'
        self.log_path = os.path.dirname(os.path.realpath(__file__)) + '/logs/'
        self.logging_file = self.log_path + self.log_file
        self.logging_level = logging.DEBUG
        self.tag = tag

        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level, format='%(tag)s %(asctime)s %(message)s')

    def debug(self, message=None):
        """
        Debug message
        """
        logging.debug(message, extra={'tag': self.tag})

    def error(self, message=None):
        """
        Error message
        """
        logging.error(message, extra={'tag': self.tag})

    def info(self, message=None):
        """
        Info message
        """
        logging.info(message, extra={'tag': self.tag})

    def warning(self, message=None):
        """
        Warning message
        """
        logging.warning(message, extra={'tag': self.tag})
