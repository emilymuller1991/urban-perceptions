import logging
from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("testing")
        self.logger.setLevel(logging.INFO)

    # def set_console_handler(self):
    #     """ """
    #     ch = logging.StreamHandler()
    #     ch.setLevel(logging.ERROR)

    #     # create and add formatter to handle
    #     formatter = logging.Formatter(
    #         fmt="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s(%(lineno)d): %("
    #         "message)s",
    #         datefmt="%Y/%m/%d %H:%M:%S",
    #     )
    #     ch.setFormatter(formatter)

    #     # add ch to logger
    #     self._logger.addHandler(ch)


def set_file_handler(logger, run_name):
    """ """
    file_path = Path(__file__).parent.parent
    filename = (
        file_path
        / "outputs"
        / "logger"
        / (run_name + f"{datetime.now().strftime('%Y%m%d_%H-%M-%S')}.log")
    )
    ch = logging.FileHandler(str(filename))
    ch.setLevel(logging.INFO)

    # create and add formatter to handle
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
    )
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


logger = Logger().logger
