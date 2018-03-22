from functools import wraps
from flask import abort, flash, url_for, redirect, request, Response
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email
from flask_babel import lazy_gettext as _


class LoginForm(FlaskForm):
    email = StringField(_('E-mail'), validators=[Required(), Email()])
    password = PasswordField(_('Password'), validators=[Required()])
    remember_me = BooleanField(_('Remember me'))
    submit = SubmitField(_('Log on'))


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_role(role):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def must_be_admin(f):
    return role_required('administrator')(f)
