from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import Required, Email, EqualTo


class UserCreateForm(Form):
    email = StringField('E-mail', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password_match',
                                                                         message='Passwords must match')])
    password_match = PasswordField('Confirm password', validators=[Required()])
    roles = SelectMultipleField('Role', validators=[Required()], coerce=int)
    submit = SubmitField('Create')


class UserModifyForm(Form):
    email = StringField('E-mail', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[EqualTo('password_match',
                                                             message='Passwords must match')])
    password_match = PasswordField('Confirm password', validators=[])
    roles = SelectMultipleField('Role', validators=[Required()], coerce=int)
    submit = SubmitField('Edit')


class UserDeleteForm(Form):
    submit = SubmitField('Confirm delete')
