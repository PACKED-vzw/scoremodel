from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_babel import lazy_gettext as _


class GenericCreateForm(Form):
    name = StringField(_('Name'), validators=[Required()])
    submit = SubmitField(_('Submit'))


class GenericDeleteForm(Form):
    submit = SubmitField(_('Confirm delete'))
