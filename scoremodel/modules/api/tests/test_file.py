from scoremodel.modules.api.document import DocumentApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.file import FileApi
from scoremodel.modules.api.tests import *
from flask import url_for
from werkzeug.utils import secure_filename
import io


class FileTest(ApiTest):

    def test_create(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id})
        r = self.client.post(url_for('admin.v_login'), data={'email': 'admin@packed.be', 'password': 'admin'})
        self.assert_redirects(r, url_for('site.v_index'))
        data = dict(input_file=((io.BytesIO(b'test')), 'test.png'))
        r = self.client.post(url_for('api.v_api_document_resource_upload', document_id=d.id),
                             content_type='multipart/form-data', data=data)
        self.assert200(r)
        d_u = DocumentApi().read(d.id)
        assert d_u.filename == secure_filename('test.png')
        assert d_u.original_filename == 'test.png'

    def test_read(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id})
        r = self.client.post(url_for('admin.v_login'), data={'email': 'admin@packed.be', 'password': 'admin'})
        data = dict(input_file=((io.BytesIO(b'test')), 'test.png'))
        r = self.client.post(url_for('api.v_api_document_resource_upload', document_id=d.id),
                             content_type='multipart/form-data', data=data)
        f = FileApi().read('test.png')
        assert f['filename'] == secure_filename('test.png')

    def test_update(self):
        # Unsupported via the API/Not used
        pass

    def test_delete(self):
        en = LangApi().by_lang('en')
        d = DocumentApi().create({'name': 'Foo', 'lang_id': en.id})
        r = self.client.post(url_for('admin.v_login'), data={'email': 'admin@packed.be', 'password': 'admin'})
        data = dict(input_file=((io.BytesIO(b'test')), 'test.png'))
        r = self.client.post(url_for('api.v_api_document_resource_upload', document_id=d.id),
                             content_type='multipart/form-data', data=data)
        assert FileApi().delete('test.png') is True
