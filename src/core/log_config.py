import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


class Logger:
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    LOG_FORMAT = "[%(asctime)s] %(name)15s:%(lineno)-3d %(levelname)-8s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, name: str = "app_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.hasHandlers():
            self.logger.addHandler(self._get_file_handler())
            self.logger.addHandler(self._get_console_handler())
            self.logger.propagate = False

    def _get_file_handler(self):
        file_handler = TimedRotatingFileHandler(
            filename=self.LOG_FILE,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
        )
        formatter = logging.Formatter(self.LOG_FORMAT, datefmt=self.DATE_FORMAT)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        return file_handler

    def _get_console_handler(self):
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(self.LOG_FORMAT, datefmt=self.DATE_FORMAT)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        return console_handler

    def get_logger(self):
        return self.logger
