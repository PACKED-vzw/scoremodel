from functools import wraps
from flask import abort, flash, url_for, redirect, request, Response
from flask.ext.login import current_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email
from flask.ext.babel import lazy_gettext as _


class LoginForm(Form):
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


def must_be_editor(f):
    return role_required('editor')(f)


def must_be_registered(f):
    return role_required('registered')(f)


##
# Basic Authentication (debugging only)
##
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

