import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

##
# Database settings
##
DB_HOST = 'localhost'
DB_NAME = 'scoremodel'
DB_USER = 'scoremodel'
DB_PASS = 'scoremodel'

##
# Flask-WTF
##
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret_key'

##
# Babel
##
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'
LANGUAGES = ['nl', 'en']

##
# Uploads
##
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passw}@{host}/{db}'.format(user=DB_USER, passw=DB_PASS,
                                                                      host=DB_HOST, db=DB_NAME)
