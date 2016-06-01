from flask import session
from flask.ext.login import current_user
from scoremodel import app


class Locale:

    def __init__(self):
        pass

    @property
    def current_locale(self):
        return self.get_current_locale()

    def get_current_locale(self):
        if 'locale' in session:
            return session['locale']
        if current_user.is_anonymous or not current_user.locale:
            return app.config['BABEL_DEFAULT_LOCALE']
        return current_user.locale

    def set_session_locale(self, new_locale):
        if new_locale in app.config['LANGUAGES']:
            session['locale'] = new_locale
            return True
        else:
            return False
