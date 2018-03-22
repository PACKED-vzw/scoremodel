from flask_babel import gettext as _
from sqlalchemy import and_, or_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.pages import Page, Lang, MenuLink
from scoremodel.modules.api.menu_link import MenuLinkApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class PageApi(GenericApi):
    simple_params = ['menu_link_id', 'content', 'lang_id']
    complex_params = []
    required_params = ['menu_link_id']
    possible_params = simple_params + complex_params

    def __init__(self):
        self.lang_api = LangApi()
        self.menu_link_api = MenuLinkApi()

    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        if not cleaned_data['lang_id']:
            cleaned_data['lang_id'] = 1
        # Language
        existing_lang = self.lang_api.read(cleaned_data['lang_id'])
        # Menu link
        existing_menu_link = self.menu_link_api.read(cleaned_data['menu_link_id'])
        existing_page = Page.query.filter(and_(Page.menu_link_id == existing_menu_link.id,
                                               Page.lang_id == existing_lang.id)).first()
        # There can not be two pages with the same lang_id and menu_link_id
        if existing_page:
            raise DatabaseItemAlreadyExists(_('A page for menu_link {0} in language {1} already exists.')
                                            .format(cleaned_data['menu_link_id'], cleaned_data['lang_id']))

        new_page = Page(content=cleaned_data['content'])
        new_page.lang = existing_lang
        new_page.menu_link = existing_menu_link
        db.session.add(new_page)
        db.session.commit()
        return new_page

    def read(self, page_id):
        existing_page = Page.query.filter(Page.id == page_id).first()
        if not existing_page:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Page, page_id))
        return existing_page

    def update(self, page_id, input_data):
        cleaned_data = self.parse_input_data(input_data)
        existing_page = self.read(page_id)
        existing_page.content = cleaned_data['content']
        # Language
        if not cleaned_data['lang_id']:
            cleaned_data['lang_id'] = 1
        existing_lang = self.lang_api.read(cleaned_data['lang_id'])
        # Menu link
        existing_menu_link = self.menu_link_api.read(cleaned_data['menu_link_id'])
        existing_page.lang = existing_lang
        existing_page.menu_link = existing_menu_link
        db.session.commit()
        return existing_page

    def delete(self, page_id):
        existing_page = self.read(page_id)
        db.session.delete(existing_page)
        db.session.commit()
        return True

    def list(self):
        all_pages = Page.query.all()
        return all_pages

    def by_lang(self, lang):
        # Language
        existing_lang = self.lang_api.by_lang(lang)
        return Page.query.filter(Page.lang_id == existing_lang.id).all()

    def by_menu_link(self, menu_link):
        # Menu link
        existing_menu_link = self.menu_link_api.by_menu_link(menu_link)
        return Page.query.filter(Page.menu_link_id == existing_menu_link.id).all()

    def by_menu_link_and_lang(self, menu_link, lang):
        # Language
        existing_lang = self.lang_api.by_lang(lang)
        # Menu link
        existing_menu_link = self.menu_link_api.by_menu_link(menu_link)
        existing_page = Page.query.filter(and_(Page.menu_link_id == existing_menu_link.id,
                                               Page.lang_id == existing_lang.id)).first()
        if not existing_page:
            raise DatabaseItemDoesNotExist(_('A page for menu_link {0} in language {1} does not exist.')
                                           .format(menu_link, lang))
        return existing_page

    def parse_input_data(self, input_data):
        return self.clean_input_data(Page, input_data, possible_params=self.possible_params,
                                     complex_params=self.complex_params,
                                     required_params=self.required_params)
