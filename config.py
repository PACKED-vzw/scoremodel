import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

##
# Database settings
##
DB_HOST = 'localhost'
DB_NAME = 'scoremodel'
DB_USER = 'scoremodel'
DB_PASS = 'password'

##
# Flask-WTF
##
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret_key'



##
# Debug settings
##
if DEBUG is True:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passw}@{host}/{db}'.format(user=DB_USER, passw=DB_PASS,
                                                                           host=DB_HOST, db=DB_NAME)
