from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.babel import lazy_gettext as _


class ReportCreateForm(Form):
    title = StringField(_('Title'), validators=[Required()])
    submit = SubmitField(_('Create'))


class ReportDeleteForm(Form):
    submit = SubmitField(_('Confirm delete'))
