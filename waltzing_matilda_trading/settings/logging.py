from config import config
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # You can add more handlers like FileHandler, etc.
    },
    'root': {
        'handlers': ['console'],
        'level': config.logging_level,
    },
}

# Configure Django's default logging
logging.config.dictConfig(LOGGING)
