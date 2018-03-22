from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired
from flask_babel import lazy_gettext as _


class UserReportCreateForm(Form):
    name = StringField(_('Report name'), validators=[InputRequired()])
    report = SelectField(_('Report template'), validators=[InputRequired()], coerce=int)
    submit = SubmitField(_('Save'))
