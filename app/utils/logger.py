import logging
from app.config.logging_config import setup_logging

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            setup_logging()
        return cls._instance

logger = Logger()