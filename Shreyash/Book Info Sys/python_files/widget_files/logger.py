import logging
import os
import sys
from typing import Optional


class Log:
    def __init__(self, log_file : str):
        self.log_file = log_file
        if not os.path.isfile(self.log_file) :
            try :
                with open (self.log_file, "w") as f :
                    pass
            except PermissionError :
                print("!ERROR : Logging disabled", file=sys.stderr)

        if os.path.isfile(self.log_file) :
            logging.basicConfig(filename=self.log_file, filemode='a', datefmt='%d/%m/%y\t%H:%M:%S',\
                                format='%(asctime)s \t%(name)-8s %(levelname)-8s %(message)-8s')

            self.logger = logging.getLogger("BookAppLogger")
            self.logger.setLevel(logging.DEBUG)
    
    def debug_logger(self, message : str) -> None :
        '''Logs message in debug mode'''
        if os.path.isfile(self.log_file) :
            self.logger.debug(message)
    def info_logger(self, message : str) -> None :
        '''Logs message in info mode'''
        if os.path.isfile(self.log_file) :
            self.logger.info(message)
    def warning_logger(self, message : str) -> None :
        '''Logs message in warning mode'''
        if os.path.isfile(self.log_file) :
                self.logger.warning(message)
    def error_logger(self, message : str) -> None :
        '''Logs message in error mode'''
        if os.path.isfile(self.log_file) :
            self.logger.error(message)
    def critical_logger(self, message : str) -> None :
        '''Logs message in critical mode'''
        if os.path.isfile(self.log_file) :
            self.logger.critical(message)