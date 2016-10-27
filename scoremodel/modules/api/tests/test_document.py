from scoremodel.modules.api.document import DocumentApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.tests import *


class DocumentTest(ApiTest):

    def test_create(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id})
        assert d in scoremodel.db.session
        self.assertRaises(DatabaseItemAlreadyExists, DocumentApi().create, {'name': 'Foo', 'lang_id': en.id})

    def test_read(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id, 'filename': 'foo.txt'})
        assert d == DocumentApi().read(d.id)
        assert d.id in [i.id for i in DocumentApi().by_filename('foo.txt')]

    def test_update(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id})
        d_u = DocumentApi().update(d.id, {'name': 'Bar', 'lang_id': en.id})
        assert d_u.name == 'Bar'
        assert d_u.id == d.id
        assert d_u == DocumentApi().read(d.id)

    def test_delete(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id})
        assert DocumentApi().delete(d.id) is True
        assert d not in scoremodel.db.session

    def test_set_filenames(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id, 'filename': 'foo.txt', 'original_filename': 'bar.txt'})
        d_x = DocumentApi().set_filenames(d.id, filename='renamed.txt', original_filename='notrenamed.txt')
        assert d_x.filename == 'renamed.txt'
        assert d_x.original_filename == 'notrenamed.txt'
        assert DocumentApi().read(d.id).filename == 'renamed.txt'
        assert DocumentApi().read(d.id).original_filename == 'notrenamed.txt'
