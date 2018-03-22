from flask_babel import gettext as _
from sqlalchemy import and_, or_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.pages import Lang
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist,\
    MethodNotImplemented
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class LangApi(GenericApi):

    simple_params = ['lang']
    complex_params = []
    required_params = ['lang']
    possible_params = simple_params + complex_params
    
    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        existing_lang = Lang.query.filter(Lang.lang == cleaned_data['lang']).first()
        if existing_lang:
            raise DatabaseItemAlreadyExists(_e['item_exists'].format(Lang, cleaned_data['lang']))
        new_lang = Lang(lang=cleaned_data['lang'])
        db.session.add(new_lang)
        db.session.commit()
        return new_lang

    def list(self):
        return Lang.query.all()

    def read(self, lang_id):
        existing_lang = Lang.query.filter(Lang.id == lang_id).first()
        if not existing_lang:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Lang, lang_id))
        return existing_lang

    def update(self, lang_id, input_data):
        raise MethodNotImplemented

    def delete(self, lang_id):
        existing_lang = self.read(lang_id)
        db.session.delete(existing_lang)
        db.session.commit()
        return True

    def by_lang(self, lang):
        existing_lang = Lang.query.filter(Lang.lang == lang).first()
        if not existing_lang:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Lang, lang))
        return existing_lang

    def parse_input_data(self, input_data):
        return self.clean_input_data(Lang, input_data, self.possible_params, self.required_params, self.complex_params)
