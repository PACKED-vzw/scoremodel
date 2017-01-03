import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

##
# Database settings
##
DB_HOST = 'localhost'
DB_NAME = 'scoremodel'
DB_USER = 'travis'
DB_PASS = ''
##
# MySQL SSL connections
##
use_ssl = False
SSL_CA = '/etc/mysql/certs/ca-cert.pem'
SSL_KEY = '/etc/mysql/keys/client-key.pem'
SSL_CERT = '/etc/mysql/certs/client-cert.pem'

##
# Flask-WTF
##
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret_key'

##
# Log-in
##
REMEMBER_COOKIE_SECURE = True
REMEMBER_COOKIE_HTTPONLY = True
SESSION_PROTECTION = "strong"

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

##
# Logger
##
LOG_FILENAME = 'logs/scoremodel.log'

if use_ssl is True:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{passw}@{host}/{db}?ssl_key={ssl_key}&ssl_cert={ssl_cert}'.format(
            user=DB_USER, passw=DB_PASS,
            host=DB_HOST, db=DB_NAME, ssl_key=SSL_KEY, ssl_cert=SSL_CERT)
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{passw}@{host}/{db}'.format(user=DB_USER, passw=DB_PASS,
                                                                              host=DB_HOST, db=DB_NAME)
