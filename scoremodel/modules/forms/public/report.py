from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired


class UserReportCreateForm(Form):
    name = StringField('Naam', validators=[InputRequired()])
    report = SelectField('Basisrapport', validators=[InputRequired()], coerce=int)
    submit = SubmitField('Opslaan')
