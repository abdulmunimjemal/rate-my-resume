import logging
from logging.config import dictConfig

def setup_logging():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "app.log",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",  # Change to INFO to capture more detailed logs
        },
    }
    dictConfig(logging_config)
