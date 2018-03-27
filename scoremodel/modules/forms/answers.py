from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired
from flask_babel import lazy_gettext as _


class AnswerCreateForm(Form):
    answer = StringField(_('Answer'), validators=[InputRequired()])
    value = IntegerField(_('Value'), validators=[InputRequired()], default=0)
    lang = SelectField(_('Language'), validators=[InputRequired()], coerce=int)
    submit = SubmitField(_('Submit'))
