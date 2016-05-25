from flask.ext.babel import gettext as _
from sqlalchemy import and_, or_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.pages import Page
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class PageApi(GenericApi):
    simple_params = ['menu_link', 'content', 'lang']
    complex_params = []
    required_params = ['menu_link', 'content']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        # There can not be two pages for which menu_link and lang are equal
        if not cleaned_data['lang']:
            cleaned_data['lang'] = 'nl'
        existing_page = Page.query.filter(and_(Page.menu_link == cleaned_data['menu_link'],
                                          Page.lang == cleaned_data['lang'])).first()
        if existing_page:
            raise DatabaseItemAlreadyExists(_('A page for menu_link {0} in language {1} already exists.')
                                            .format(cleaned_data['menu_link'], cleaned_data['lang']))
        new_page = Page(menu_link=cleaned_data['menu_link'], content=cleaned_data['content'], lang=cleaned_data['lang'])
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
        existing_page = self.update_simple_attributes(existing_page, self.simple_params, cleaned_data)
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
        return Page.query.filter(Page.lang == lang).all()

    def by_menu_link(self, menu_link):
        return Page.query.filter(Page.menu_link == menu_link).all()

    def by_menu_link_and_lang(self, menu_link, lang):
        existing_page = Page.query.filter(and_(Page.menu_link == menu_link,
                                               Page.lang == lang)).first()
        if not existing_page:
            raise DatabaseItemDoesNotExist(_('A page for menu_link {0} in language {1} does not exist.')
                                            .format(menu_link, lang))
        return existing_page

    def parse_input_data(self, input_data):
        return self.clean_input_data(Page, input_data, possible_params=self.possible_params,
                                     complex_params=self.complex_params,
                                     required_params=self.required_params)
