from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.user import UserApi
from scoremodel.models.public import UserReport
from scoremodel.modules.api.tests import *


class UserReportTest(ApiTest):

    def test_create(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        o = UserReportApi().create({'name': 'Test', 'user_id': u.id, 'report_id': r.id})
        assert o in scoremodel.db.session
        # No checking for already_exists
        self.assertIsInstance(o, UserReport)

    def test_read(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        o = UserReportApi().create({'name': 'Test', 'user_id': u.id, 'report_id': r.id})
        assert o == UserReportApi().read(o.id)

    def test_update(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        o = UserReportApi().create({'name': 'Test', 'user_id': u.id, 'report_id': r.id})
        o_x = UserReportApi().update(o.id, {'name': 'Foo', 'user_id': u.id, 'report_id': r.id})
        assert o_x == UserReportApi().read(o.id)
        assert UserReportApi().read(o.id).name == 'Foo'
        self.assertIsInstance(o_x, UserReport)

    def test_delete(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        u = UserApi().create({'email': 'foo@bar.be', 'password': '123'})
        o = UserReportApi().create({'name': 'Test', 'user_id': u.id, 'report_id': r.id})
        assert UserReportApi().delete(o.id) is True
        assert o not in scoremodel.db.session
