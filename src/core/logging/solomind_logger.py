
import logging
from logging.handlers import RotatingFileHandler
import os 
from datetime import datetime

class SolomindLoggerOptions:
    def __init__(self, log_file_path:str, log_level:str) -> None:
        self.log_file_path:str = log_file_path
        self.log_level:str = log_level
        
class SolomindLogger:
    def  __init__(self, options:SolomindLoggerOptions) -> None:
        self.options = options
        self.__log_level__ = logging.getLevelName(options.log_level())

        date_time_string = datetime.now().strftime('%Y-%m-%d')
        self.__log_file_full_path__ = f"{self.options.log_file_path()}/{date_time_string}_solomind.log" 

        self.__create_file_and_folder__()

    def create_logger(self):
        rfh = RotatingFileHandler(
            filename=self.__log_file_full_path__, 
            mode='a',
            maxBytes=5*1024*1024,
            backupCount=2,
            encoding='utf-8',
            delay=0
        )

        logging.basicConfig(
            level=self.__log_level__,
            format="%(asctime)s %(levelname)-8s %(name)-25s %(message)s",
            datefmt="%y-%m-%d %H:%M:%S",
            handlers=[
                rfh
            ]
        )
    
    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.level =self.__log_level__
        return logger;

    def __create_file_and_folder__(self):
        os.makedirs(os.path.dirname(self.__log_file_full_path__), exist_ok=True)
        _ = open(self.__log_file_full_path__, 'a')
        
