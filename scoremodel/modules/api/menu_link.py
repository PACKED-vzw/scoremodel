from flask.ext.babel import gettext as _
from sqlalchemy import and_, or_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.pages import MenuLink
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class MenuLinkApi(GenericApi):

    def list(self):
        return MenuLink.query.all()

    def read(self, menu_link_id):
        existing_menu_link = MenuLink.query.filter(MenuLink.id == menu_link_id).first()
        if not existing_menu_link:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(MenuLink, menu_link_id))
        return existing_menu_link

    def by_menu_link(self, menu_link):
        existing_menu_link = MenuLink.query.filter(MenuLink.menu_link == menu_link).first()
        if not existing_menu_link:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(MenuLink, menu_link))
        return existing_menu_link
