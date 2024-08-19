from loguru import logger
import sys


class CustomLogger:
    def __init__(self):
        self.configure_logger()

    def configure_logger(self):
        logger.remove()  # Remove the default logger
        logger.add(sys.stdout, level="DEBUG")  # Add stdout handler
        logger.add(
            "logs/file_{time}.log", rotation="1 MB"
        )  # Add file handler with rotation

    def get_logger(self):
        return logger


custom_logger = CustomLogger().get_logger()
