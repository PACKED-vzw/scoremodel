from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired
from flask.ext.babel import lazy_gettext as _


class UserReportCreateForm(Form):
    name = StringField(_('Naam'), validators=[InputRequired()])
    report = SelectField(_('Basisrapport'), validators=[InputRequired()], coerce=int)
    submit = SubmitField(_('Opslaan'))
