from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.models.general import Section
from scoremodel.modules.api.tests import *


class SectionTest(ApiTest):

    def test_create(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        assert s in scoremodel.db.session
        assert s.order_in_report == 0
        self.assertIsInstance(s, Section)
        self.assertRaises(DatabaseItemAlreadyExists, SectionApi().create, {'title': 'Test', 'report_id': r.id})

    def test_read(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        assert s == SectionApi().read(s.id)

    def test_update(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        s_u = SectionApi().update(s.id, {'title': 'Toto', 'report_id': r.id, 'order_in_report': 1})
        assert s_u == SectionApi().read(s.id)
        assert SectionApi().read(s.id).title == 'Toto'
        assert SectionApi().read(s.id).order_in_report == 1
        self.assertIsInstance(s_u, Section)

    def test_delete(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        assert SectionApi().delete(s.id) is True
        assert s not in scoremodel.db.session

    def test_complex(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id, 'order_in_report': 2, 'weight': 5})
        assert s in scoremodel.db.session
        assert s.order_in_report == 2
        assert s.weight == 5
        self.assertIsInstance(s, Section)