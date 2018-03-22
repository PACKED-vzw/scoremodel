from flask import session
from flask_login import current_user
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel import app


class Locale:

    def __init__(self):
        pass

    @property
    def current_locale(self):
        return self.get_current_locale()

    @property
    def fallback_locale(self):
        return app.config['BABEL_DEFAULT_LOCALE']

    def get_current_locale(self):
        if 'locale' in session:
            return session['locale']
        if not current_user:
            return app.config['BABEL_DEFAULT_LOCALE']
        if current_user.is_anonymous or not current_user.locale:
            return app.config['BABEL_DEFAULT_LOCALE']
        return current_user.locale

    def set_session_locale(self, new_locale):
        if new_locale in app.config['LANGUAGES']:
            session['locale'] = new_locale
            return True
        else:
            return False

    def set_locale(self, new_locale):
        user_api = UserApi()
        if new_locale in app.config['LANGUAGES']:
            if self.set_session_locale(new_locale) is True:
                if current_user.is_authenticated:
                    try:
                        user_api.set_locale(current_user.id, new_locale)
                    except DatabaseItemDoesNotExist:
                        return False
                return True
        return False
