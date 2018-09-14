import logging
import logging.handlers
import sys

from settings import log_level


def set_log_level(level):
    switcher = {
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL
    }
    return switcher.get(level.upper(), "Invalid LOG LEVEL")


# noinspection PyShadowingNames
def init_logging(log_file):
    s = f'[%(asctime)s][%(name)s][%(levelname)s]: %(message)s'
    logging.basicConfig(format=s, level=set_log_level(log_level))
    formatter = logging.Formatter(s)

    fh = logging.handlers.TimedRotatingFileHandler(filename=f"{log_file}.log", when='MIDNIGHT', backupCount=7, utc=True)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logging.getLogger('').addHandler(fh)


# noinspection PyShadowingNames
def close_logging():
    for handler in logging.getLogger('').handlers:
        handler.close()


# noinspection PyShadowingBuiltins
def failure_logging(message, logger="", exit=True, level="ERROR"):
    logger = logging.getLogger(logger)
    if level == "WARN":
        logger.warning(message)
    else:
        logger.error(message)
    if exit:
        logger.info("CALLING PROCESS EXIT")
        sys.exit(1)
