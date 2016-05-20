from flask.ext.wtf import Form
from flask.ext.babel import gettext as _
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField(_('Gebruikersnaam'), validators=[DataRequired()])
    password = PasswordField(_('Wachtwoord'), validators=[DataRequired()])
    remember_me = BooleanField(_('Onthouden'), default=False)
