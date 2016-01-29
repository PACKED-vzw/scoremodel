from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class GenericCreateForm(Form):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Create')


class GenericDeleteForm(Form):
    submit = SubmitField('Confirm delete')