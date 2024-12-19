import logging as log
from src.commons.Serializable import Serializable

class LoggerInitializer(Serializable):
    def __init__(self, level=log.WARN, filepath = None):
        log.basicConfig(
            level=log.DEBUG,
            format='[%(asctime)s]\t%(levelname)s\t%(filename)s > %(funcName)s\t%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filemode="a",
            filename=filepath
        )