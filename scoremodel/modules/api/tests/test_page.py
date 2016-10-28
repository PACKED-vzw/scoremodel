from scoremodel.modules.api.page import PageApi
from scoremodel.modules.api.menu_link import MenuLinkApi
from scoremodel.models.pages import Page
from scoremodel.modules.api.tests import *


class PageTest(ApiTest):

    def test_create(self):
        v_index = MenuLinkApi().by_menu_link('v_index')
        p = PageApi().create({'menu_link_id': v_index.id})
        assert p in scoremodel.db.session
        self.assertRaises(DatabaseItemAlreadyExists, PageApi().create, {'menu_link_id': v_index.id})
        self.assertIsInstance(p, Page)

    def test_read(self):
        v_index = MenuLinkApi().by_menu_link('v_index')
        p = PageApi().create({'menu_link_id': v_index.id})
        assert p == PageApi().read(p.id)

    def test_update(self):
        v_index = MenuLinkApi().by_menu_link('v_index')
        v_faq = MenuLinkApi().by_menu_link('v_faq')
        p = PageApi().create({'menu_link_id': v_index.id})
        p_x = PageApi().update(p.id, {'menu_link_id': v_faq.id})
        assert p_x == PageApi().read(p.id)
        assert PageApi().read(p.id).menu_link_id == v_faq.id
        self.assertIsInstance(p_x, Page)

    def test_delete(self):
        v_index = MenuLinkApi().by_menu_link('v_index')
        p = PageApi().create({'menu_link_id': v_index.id})
        assert PageApi().delete(p.id) is True
        assert p not in scoremodel.db.session
