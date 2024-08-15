import logging


def setup_logger():
    logger = logging.getLogger("my_app_logger")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    return logger


logger = setup_logger()
