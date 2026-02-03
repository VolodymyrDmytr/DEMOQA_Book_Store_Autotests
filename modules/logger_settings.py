import logging
from logging import FileHandler, StreamHandler, Formatter, DEBUG, ERROR


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(DEBUG)

    if root_logger.handlers:
        return

    formatter = Formatter(
        '%(asctime)s : %(name)s : %(levelname)s : %(message)s',
    )

    file_handler = FileHandler('Log_file.log', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = StreamHandler()
    console_handler.setLevel(ERROR)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
