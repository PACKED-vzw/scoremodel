from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.tests import *
from scoremodel.models.user import User


class UserTest(ApiTest):

    def test_create(self):
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        assert u in scoremodel.db.session
        assert 'public' in [r.role for r in u.roles]
        self.assertIsInstance(u, User)

    def test_read(self):
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        u = UserApi().get_by_user('foo@bar.be')
        assert u.email == 'foo@bar.be'
        u_id = UserApi().read(u.id)
        assert u.id == u_id.id
        assert UserApi().check_password(u.id, '123')
        self.assertRaises(InvalidPassword, UserApi().check_password, u.id, '456')

    def test_update(self):
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        u = UserApi().get_by_user('foo@bar.be')
        u_u = UserApi().update(u.id, {'password': '456', 'email': 'x@y.be'})
        assert u_u.email == 'x@y.be'
        u_x = UserApi().read(u.id)
        assert u_x.email == u_u.email
        assert UserApi().check_password(u_x.id, '456')
        self.assertIsInstance(u_u, User)

    def test_delete(self):
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        assert UserApi().delete(u.id)
        assert u not in scoremodel.db.session
