from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.tests import *
from scoremodel.models.general import RiskFactor


class RiskFactorTest(ApiTest):

    def test_create(self):
        en = LangApi().by_lang('en')
        r = RiskFactorApi().create({'risk_factor': 'Test', 'lang_id': en.id})
        assert r in scoremodel.db.session
        assert r.value == 1
        r_a = RiskFactorApi().create({'risk_factor': 'ValueTest', 'lang_id': en.id, 'value': 5})
        assert r_a.value == 5
        self.assertRaises(DatabaseItemAlreadyExists, RiskFactorApi().create, {'risk_factor': 'Test', 'lang_id': en.id})
        self.assertIsInstance(r, RiskFactor)

    def test_read(self):
        en = LangApi().by_lang('en')
        r = RiskFactorApi().create({'risk_factor': 'Test', 'lang_id': en.id})
        assert r == RiskFactorApi().read(r.id)

    def test_update(self):
        en = LangApi().by_lang('en')
        r = RiskFactorApi().create({'risk_factor': 'Test', 'lang_id': en.id})
        r_b = RiskFactorApi().update(r.id, {'risk_factor': 'Foobar', 'lang_id': en.id})
        assert r_b.risk_factor == 'Foobar'
        assert r_b == RiskFactorApi().read(r.id)
        assert RiskFactorApi().read(r.id).risk_factor == 'Foobar'
        self.assertIsInstance(r_b, RiskFactor)

    def test_delete(self):
        en = LangApi().by_lang('en')
        r = RiskFactorApi().create({'risk_factor': 'Test', 'lang_id': en.id})
        assert RiskFactorApi().delete(r.id) is True
        assert r not in scoremodel.db.session
