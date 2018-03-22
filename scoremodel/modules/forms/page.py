from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired
from flask_babel import lazy_gettext as _


class PageCreateForm(Form):
    menu_link = SelectField(_('Menu link'), validators=[InputRequired()], coerce=int)
    lang = SelectField(_('Language'), validators=[InputRequired()], coerce=int)
    submit = SubmitField(_('Submit'))
