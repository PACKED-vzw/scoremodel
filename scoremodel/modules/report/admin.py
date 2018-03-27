from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, InputRequired
from flask_babel import lazy_gettext as _


class ReportCreateForm(Form):
    title = StringField(_('Title'), validators=[InputRequired()])
    lang = SelectField(_('Language'), validators=[InputRequired()], coerce=int)
    submit = SubmitField(_('Create'))


class ReportDeleteForm(Form):
    submit = SubmitField(_('Confirm delete'))
