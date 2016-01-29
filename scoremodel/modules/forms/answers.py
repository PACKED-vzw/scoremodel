from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired


class AnswerCreateForm(Form):
    answer = StringField('Answer', validators=[InputRequired()])
    value = IntegerField('Value', validators=[InputRequired()], default=0)
    submit = SubmitField('Submit')
