from flask import Flask
from os.path import join


class AppSetup:
    def __init__(self):
        self.app = Flask('scoremodel')
        self.app.config.from_object('config')
        self.app.config['UPLOAD_FULL_PATH'] = join(self.app.config['basedir'], 'scoremodel',
                                                   self.app.config['UPLOAD_FOLDER'])
