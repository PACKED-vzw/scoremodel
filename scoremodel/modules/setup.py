from flask import Flask


class AppSetup:
    def __init__(self):
        self.app = Flask('scoremodel')
        self.app.config.from_object('config')
