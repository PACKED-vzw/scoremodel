from scoremodel.modules.api.menu_link import MenuLinkApi
from scoremodel.models.pages import MenuLink
from scoremodel.modules.api.tests import *


class MenuLinkTest(ApiTest):

    def test_create(self):
        m = MenuLinkApi().create({'menu_link': 'id_test'})
        assert m in scoremodel.db.session
        self.assertRaises(DatabaseItemAlreadyExists, MenuLinkApi().create, {'menu_link': 'id_test'})
        self.assertIsInstance(m, MenuLink)

    def test_read(self):
        m = MenuLinkApi().create({'menu_link': 'id_test'})
        assert MenuLinkApi().read(m.id) == m

    def test_update(self):
        self.assertRaises(MethodNotImplemented, MenuLinkApi().update, '', {})

    def test_delete(self):
        self.assertRaises(MethodNotImplemented, MenuLinkApi().delete, '')
