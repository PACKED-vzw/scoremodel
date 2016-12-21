import logging
import logging.handlers
from scoremodel import app


class ScoremodelLogger:

    def __init__(self):
        self.logger = logging.getLogger('scoremodel')

        self.log_filename = app.config['LOG_FILENAME']
        if app.debug is True:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)
        self.logger.addHandler(self.make_handler())

    def make_handler(self):
        handler = logging.handlers.RotatingFileHandler(
            self.log_filename,
            maxBytes=10 * 1024,
            backupCount=5
        )
        formatter = logging.Formatter(
            '{asctime}:{levelname}:{message}',
            style='{'
        )
        handler.setFormatter(formatter)
        return handler
