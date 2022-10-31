"""Contain logging configuration."""
import sys

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(filename)s %(funcName)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'standard_console': {
            'format': '%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard_console',
            'stream': sys.stderr,
        },
        'file_loger': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'Page_loader.log',
        },
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['file_loger'],
        },
        'console_logger': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
}
