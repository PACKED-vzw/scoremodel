from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired
from flask_babel import lazy_gettext as _


class RiskFactorCreateForm(Form):
    risk_factor = StringField(_('Risk Factor'), validators=[InputRequired()])
    value = IntegerField(_('Value'), validators=[InputRequired()], default=1)
    lang = SelectField(_('Language'), validators=[InputRequired()], coerce=int)
    submit = SubmitField(_('Submit'))
