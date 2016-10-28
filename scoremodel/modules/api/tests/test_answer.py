from scoremodel.modules.api.answer import AnswerApi
from scoremodel.models.general import Answer
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.tests import *


class AnswerTest(ApiTest):

    def test_create(self):
        en = LangApi().by_lang('en')
        a = AnswerApi().create({'answer': 'Nono', 'lang_id': en.id})
        assert a in scoremodel.db.session
        assert a.value == 1
        a_b = AnswerApi().create({'answer': 'Yesyes', 'lang_id': en.id, 'value': 5})
        assert a_b in scoremodel.db.session
        assert a_b.value == 5
        self.assertRaises(DatabaseItemAlreadyExists, AnswerApi().create, {'answer': 'Nono', 'lang_id': en.id})
        self.assertIsInstance(a, Answer)

    def test_read(self):
        en = LangApi().by_lang('en')
        a = AnswerApi().create({'answer': 'Nono', 'lang_id': en.id})
        a_b = AnswerApi().create({'answer': 'Yesyes', 'lang_id': en.id, 'value': 5})
        assert a == AnswerApi().read(a.id)
        assert len(AnswerApi().by_lang(en.lang)) == 2

    def test_update(self):
        en = LangApi().by_lang('en')
        a = AnswerApi().create({'answer': 'Nono', 'lang_id': en.id, 'value': 5})
        a_b = AnswerApi().update(a.id, {'answer': 'Yesyes', 'lang_id': en.id})
        assert a_b.answer == 'Yesyes'
        assert a_b.lang_id == en.id
        assert a_b == AnswerApi().read(a.id)
        assert a_b.value == 1  # When updating, you have to provide all the values, including the unchanged ones
        self.assertIsInstance(a_b, Answer)

    def test_delete(self):
        en = LangApi().by_lang('en')
        a = AnswerApi().create({'answer': 'Nono', 'lang_id': en.id})
        assert AnswerApi().delete(a.id) is True
        assert a not in scoremodel.db.session
