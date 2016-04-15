from flask import Flask


class AppSetup:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object('config')
