from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo
from flask.ext.babel import lazy_gettext as _


class RegistrationForm(Form):
    email = StringField(_('E-mail'), validators=[InputRequired(), Email()])
    password = PasswordField(_('Password'), validators=[InputRequired(), EqualTo('password_match',
                                                                            message=_('Passwords must match'))])
    password_match = PasswordField(_('Confirm password'), validators=[InputRequired()])
    organisation_name = StringField(_('Organisation name'))
    organisation_type = SelectField(_('Organisation type'), coerce=int)
    organisation_size = SelectField(_('Organisation size'), choices=[
        ('1', _('1')),
        ('2-5', _('2-5')),
        ('6-20', _('6-20')),
        ('>20', _('21 or more'))
    ])
    language = SelectField(_('Language'), coerce=int)
    submit = SubmitField(_('Register'))