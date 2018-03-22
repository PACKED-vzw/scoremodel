from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask_babel import lazy_gettext as _


class OrganisationTypeCreateForm(Form):
    name = StringField(_('Organisation type'), validators=[InputRequired()])
    submit = SubmitField(_('Submit'))
