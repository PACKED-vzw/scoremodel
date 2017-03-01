import logging
import logging.handlers
from scoremodel import app


class ScoremodelLogger:

    def __init__(self):
        self.logger = logging.getLogger('scoremodel')

    def error(self, error):
        self.logger.error(error)

    def warning(self, warning):
        self.logger.warn(warning)

    def info(self, info):
        self.logger.info(info)

    def exception(self, exception):
        self.logger.exception(exception)

