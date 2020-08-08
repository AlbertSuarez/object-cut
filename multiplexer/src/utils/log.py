import logging
import sys


__logger_stdout = logging.getLogger('object_cut_multiplexer')

__formatter = logging.Formatter('{%(name)s} - <%(asctime)s> - [%(levelname)-7s] - %(message)s')

__handler_stdout = logging.StreamHandler(sys.stdout)
__handler_stdout.setFormatter(__formatter)
__logger_stdout.addHandler(__handler_stdout)
__logger_stdout.setLevel(logging.INFO)


def debug(msg):
    if __logger_stdout.isEnabledFor(logging.DEBUG):
        __logger_stdout.debug(msg)


def info(msg):
    __logger_stdout.info(msg)


def warn(msg):
    __logger_stdout.warning(msg)


def error(msg):
    __logger_stdout.error(msg)


def exception(msg):
    __logger_stdout.exception(msg)
