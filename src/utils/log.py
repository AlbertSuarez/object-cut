import logging
from logging.handlers import RotatingFileHandler


__logger = logging.getLogger("covigilant_API")

__formatter = logging.Formatter(
    "{%(name)s} - <%(asctime)s> - [%(levelname)-7s] - %(message)s"
)


__handler_file = RotatingFileHandler("engine.log", maxBytes=(1048576 * 5), backupCount=7)
__handler_file.setFormatter(__formatter)
__logger.addHandler(__handler_file)
__logger.setLevel(logging.INFO)


def debug(msg):
    if __logger.isEnabledFor(logging.DEBUG):
        __logger.debug(msg)


def info(msg):
    __logger.info(msg)


def warn(msg):
    __logger.warning(msg)


def error(msg):
    __logger.error(msg)
