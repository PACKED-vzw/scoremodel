from flask_login import AnonymousUserMixin
from scoremodel import app


class ScAnonymousUser(AnonymousUserMixin):
    locale = app.config['BABEL_DEFAULT_LOCALE']
