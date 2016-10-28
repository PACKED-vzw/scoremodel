from scoremodel.modules.api.role import RoleApi
from scoremodel.modules.api.tests import *
from scoremodel.models.user import Role


class RoleTest(ApiTest):

    def test_create(self):
        r = RoleApi().create({'role': 'Test'})
        assert r in scoremodel.db.session
        self.assertIsInstance(r, Role)

    def test_read(self):
        r = RoleApi().create({'role': 'Test'})
        assert r == RoleApi().read(r.id)

    def test_update(self):
        r = RoleApi().create({'role': 'Test'})
        r_u = RoleApi().update(r.id, {'role': 'Foo'})
        assert r_u == RoleApi().read(r.id)
        assert RoleApi().read(r.id).role == 'Foo'
        self.assertIsInstance(r_u, Role)

    def test_delete(self):
        r = RoleApi().create({'role': 'Test'})
        assert RoleApi().delete(r.id) is True
        assert r not in scoremodel.db.session
