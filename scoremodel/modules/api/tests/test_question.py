from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.models.general import Question
from scoremodel.modules.error import DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.tests import *


class QuestionTest(ApiTest):

    def test_create(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        q = QuestionApi().create({'question': 'Test', 'weight': 1, 'section_id': s.id})
        assert q in scoremodel.db.session
        # This only works in a context manager, and not with self.assertRaises() - I have no idea why.
        with self.assertRaises(DatabaseItemAlreadyExists):
            x = QuestionApi().create({'question': 'Test', 'weight': 1, 'section_id': s.id})
        self.assertIsInstance(q, Question)

    def test_read(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        q = QuestionApi().create({'question': 'Test', 'weight': 1, 'section_id': s.id})
        assert q == QuestionApi().read(q.id)

    def test_update(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        q = QuestionApi().create({'question': 'Test', 'weight': 1, 'section_id': s.id})
        q_d = QuestionApi().update(q.id, {'question': 'Foo', 'weight': 1, 'section_id': s.id})
        assert q_d == QuestionApi().read(q.id)
        assert QuestionApi().read(q.id).question == 'Foo'
        self.assertIsInstance(q_d, Question)

    def test_delete(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        q = QuestionApi().create({'question': 'Test', 'weight': 1, 'section_id': s.id})
        assert QuestionApi().delete(q.id) is True
        assert q not in scoremodel.db.session

    def test_complex(self):
        en = LangApi().by_lang('en')
        r = ReportApi().create({'title': 'Test', 'lang_id': en.id})
        s = SectionApi().create({'title': 'Test', 'report_id': r.id})
        ri = RiskFactorApi().create({'risk_factor': 'Test', 'lang_id': en.id})
        a = AnswerApi().create({'answer': 'Test', 'lang_id': en.id})
        q = QuestionApi().create({'question': 'Test', 'weight': 1, 'section_id': s.id, 'answers': [a.id],
                                  'risk_factor_id': ri.id})
        assert q in scoremodel.db.session
        self.assertIsInstance(q, Question)
