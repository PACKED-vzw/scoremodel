from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.tests import *


class LangTest(ApiTest):

    def test_create(self):
        l = LangApi().create({'lang': 'zh'})
        assert l in scoremodel.db.session
        self.assertRaises(DatabaseItemAlreadyExists, LangApi().create, {'lang': 'zh'})

    def test_read(self):
        l = LangApi().create({'lang': 'zh'})
        assert LangApi().read(l.id) == l

    def test_update(self):
        self.assertRaises(MethodNotImplemented, LangApi().update, '', {})

    def test_delete(self):
        l = LangApi().create({'lang': 'zh'})
        assert LangApi().delete(l.id) is True
        assert l not in scoremodel.db.session
