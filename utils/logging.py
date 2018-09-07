import logging
import logging.handlers
import sys


# noinspection PyShadowingNames
def init_logging(log_file):
    s = f'[%(asctime)s][%(name)s][%(levelname)s]: %(message)s'
    logging.basicConfig(format=s, level=logging.DEBUG)
    formatter = logging.Formatter(s)

    fh = logging.handlers.TimedRotatingFileHandler(filename=f"{log_file}.log", when='MIDNIGHT', backupCount=7, utc=True)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logging.getLogger('').addHandler(fh)


# noinspection PyShadowingNames
def close_logging():
    for handler in logging.getLogger('').handlers:
        handler.close()


def error(message, logger=""):
    logger = logging.getLogger(logger)
    logger.error(message)
    sys.exit(1)
