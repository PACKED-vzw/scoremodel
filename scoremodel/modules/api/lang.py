from flask.ext.babel import gettext as _
from sqlalchemy import and_, or_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.pages import Lang
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class LangApi(GenericApi):

    def list(self):
        return Lang.query.all()

    def read(self, lang_id):
        existing_lang = Lang.query.filter(Lang.id == lang_id).first()
        if not existing_lang:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Lang, lang_id))
        return existing_lang

    def by_lang(self, lang):
        existing_lang = Lang.query.filter(Lang.lang == lang).first()
        if not existing_lang:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Lang, lang))
        return existing_lang
