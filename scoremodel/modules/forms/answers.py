from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired
from flask.ext.babel import lazy_gettext as _


class AnswerCreateForm(Form):
    answer = StringField(_('Answer'), validators=[InputRequired()])
    value = IntegerField(_('Value'), validators=[InputRequired()], default=0)
    submit = SubmitField(_('Submit'))
