from flask.ext.babel import gettext as _
from sqlalchemy import and_, or_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.pages import Lang
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.generic import GenericApi
from scoremodel.models.pages import Document
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel import db

# Check voor combinatie filename en lang_id


class DocumentApi(GenericApi):
    simple_params = ['filename', 'original_filename', 'description', 'lang_id']
    complex_params = []
    required_params = ['lang_id', 'original_filename']
    possible_params = simple_params + complex_params

    def __init__(self):
        self.lang_api = LangApi()

    def create(self, document_data):
        cleaned_data = self.parse_input_data(document_data)
        if not cleaned_data['lang_id']:
            cleaned_data['lang_id'] = 1
        existing_lang = self.lang_api.read(cleaned_data['lang_id'])
        # Original filename or new filename?
        existing_document = Document.query.filter(and_(Document.filename == cleaned_data['filename'],
                                                       Document.lang_id == cleaned_data['lang_id'])).first()
        if existing_document:
            raise DatabaseItemAlreadyExists(_('No two documents can have the same filename and lang_id!'))
        new_document = Document(filename=cleaned_data['filename'], original_filename=cleaned_data['original_filename'],
                                description=cleaned_data['description'])
        new_document.lang = existing_lang
        db.session.add(new_document)
        db.session.commit()
        return new_document

    def read(self, document_id):
        existing_document = Document.query.filter(Document.id == document_id).first()
        if not existing_document:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Document, document_id))
        return existing_document

    def update(self, document_id, document_data):
        existing_document = self.read(document_id)
        cleaned_data = self.parse_input_data(document_data)
        existing_lang = self.lang_api.read(cleaned_data['lang_id'])
        existing_document = self.update_simple_attributes(existing_document, self.simple_params, cleaned_data,
                                                          to_skip=['lang_id'])
        existing_document.lang = existing_lang
        db.session.commit()
        return existing_document

    def delete(self, document_id):
        existing_document = self.read(document_id)
        db.session.delete(existing_document)
        db.session.commit()
        return True

    def list(self):
        all_documents = Document.query.all()
        return all_documents

    def parse_input_data(self, input_data):
        return self.clean_input_data(Document, input_data, possible_params=self.possible_params,
                                     complex_params=self.complex_params,
                                     required_params=self.required_params)