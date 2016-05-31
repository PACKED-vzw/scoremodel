from flask import Flask
from os.path import join, exists
from os import mkdir


class AppSetup:
    def __init__(self):
        self.app = Flask('scoremodel')
        self.app.config.from_object('config')
        self.app.config['UPLOAD_FULL_PATH'] = join(self.app.config['BASEDIR'], 'scoremodel',
                                                   self.app.config['UPLOAD_FOLDER'])
        if not exists(self.app.config['UPLOAD_FULL_PATH']):
            mkdir(self.app.config['UPLOAD_FULL_PATH'], 0o755)
