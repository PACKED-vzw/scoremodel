from flask_testing import TestCase
import scoremodel
import os
from scoremodel.modules.setup.first_time import testing_db_setup
from scoremodel.modules.error import *


class ApiTest(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(scoremodel.app.config['BASEDIR'], 'test.db')
    TESTING = True
    WTF_CSRF_ENABLED = False

    def create_app(self):
        scoremodel.app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        scoremodel.app.config['WTF_CSRF_ENABLED'] = self.WTF_CSRF_ENABLED
        # wtf_csrf_enabled = true is set in scoremodel.py, which is imported here
        # so our settings are ignored. The below fixes that.
        # See https://stackoverflow.com/questions/38624060/flask-disable-csrf-in-unittest
        scoremodel.app.config['WTF_CSRF_METHODS'] = []
        scoremodel.app.config['TESTING'] = self.TESTING
        scoremodel.app.config['DEBUG'] = True
        return scoremodel.app

    def setUp(self):
        scoremodel.db.create_all()
        with scoremodel.app.app_context():
            testing_db_setup()

    def tearDown(self):
        scoremodel.db.session.remove()
        scoremodel.db.drop_all()
