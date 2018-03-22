from flask_babel import gettext as _
from sqlalchemy import and_, or_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.pages import MenuLink
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist,\
    MethodNotImplemented
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class MenuLinkApi(GenericApi):

    simple_params = ['menu_link']
    complex_params = []
    required_params = ['menu_link']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        existing_menu_link = MenuLink.query.filter(MenuLink.menu_link == cleaned_data['menu_link']).first()
        if existing_menu_link:
            raise DatabaseItemAlreadyExists(_e['item_exists'].format(MenuLink, cleaned_data['menu_link']))
        new_menu_link = MenuLink(menu_link=cleaned_data['menu_link'])
        db.session.add(new_menu_link)
        db.session.commit()
        return new_menu_link

    def list(self):
        return MenuLink.query.all()

    def read(self, menu_link_id):
        existing_menu_link = MenuLink.query.filter(MenuLink.id == menu_link_id).first()
        if not existing_menu_link:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(MenuLink, menu_link_id))
        return existing_menu_link

    def update(self, menu_link_id, input_data):
        raise MethodNotImplemented

    def delete(self, menu_link_id):
        raise MethodNotImplemented

    def by_menu_link(self, menu_link):
        existing_menu_link = MenuLink.query.filter(MenuLink.menu_link == menu_link).first()
        if not existing_menu_link:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(MenuLink, menu_link))
        return existing_menu_link

    def parse_input_data(self, input_data):
        return self.clean_input_data(MenuLink, input_data, self.possible_params, self.required_params, self.complex_params)
