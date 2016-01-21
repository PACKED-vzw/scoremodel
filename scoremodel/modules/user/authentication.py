from functools import wraps
from flask import abort
from flask.ext.login import current_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email


class LoginForm(Form):
    email = StringField('E-mail', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Onthouden')
    submit = SubmitField('Aanmelden')


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


def must_be_editor(f):
    return role_required('editor')(f)


def must_be_registered(f):
    return role_required('registered')(f)
