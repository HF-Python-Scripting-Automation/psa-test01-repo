import logging
from .logger import get_logger

def get_main_logger():
    return get_logger("Main", filename="servicename.log", level=logging.DEBUG, clear=True)