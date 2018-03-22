from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired
from flask_babel import lazy_gettext as _


class BenchmarkReportCreateForm(Form):
    name = StringField(_('Benchmark name'), validators=[InputRequired()])
    report = SelectField(_('Report template'), validators=[InputRequired()], coerce=int)
    submit = SubmitField(_('Save'))
