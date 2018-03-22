from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import Required, Email, EqualTo
from flask_babel import lazy_gettext as _


class UserCreateForm(Form):
    email = StringField(_('E-mail'), validators=[Required(), Email()])
    password = PasswordField(_('Password'), validators=[Required(), EqualTo('password_match',
                                                                            message=_('Passwords must match'))])
    password_match = PasswordField(_('Confirm password'), validators=[Required()])
    roles = SelectMultipleField(_('Role'), validators=[Required()], coerce=int)
    submit = SubmitField(_('Create'))


class UserModifyForm(Form):
    email = StringField(_('E-mail'), validators=[Required(), Email()])
    password = PasswordField(_('Password'), validators=[EqualTo('password_match',
                                                                message=_('Passwords must match'))])
    password_match = PasswordField(_('Confirm password'), validators=[])
    roles = SelectMultipleField(_('Role'), validators=[Required()], coerce=int)
    submit = SubmitField(_('Edit'))


class UserDeleteForm(Form):
    submit = SubmitField(_('Confirm delete'))
