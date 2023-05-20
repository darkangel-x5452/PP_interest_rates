import logging
import datetime

TS = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s: %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)

    return logger