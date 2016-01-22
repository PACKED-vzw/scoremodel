from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class ReportCreateForm(Form):
    title = StringField('Title', validators=[Required()])
    submit = SubmitField('Create')


class ReportDeleteForm(Form):
    submit = SubmitField('Confirm delete')
