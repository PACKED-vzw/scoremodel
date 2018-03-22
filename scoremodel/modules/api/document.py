from flask_babel import gettext as _
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
    simple_params = ['filename', 'original_filename', 'description', 'lang_id', 'name']
    complex_params = []
    required_params = ['lang_id', 'name']
    possible_params = simple_params + complex_params

    def __init__(self):
        self.lang_api = LangApi()

    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        if not cleaned_data['lang_id']:
            cleaned_data['lang_id'] = 1
        existing_lang = self.lang_api.read(cleaned_data['lang_id'])
        existing_document = Document.query.filter(and_(Document.name == cleaned_data['name'],
                                                       Document.lang_id == cleaned_data['lang_id'])).first()
        if existing_document:
            raise DatabaseItemAlreadyExists(_('No two documents can have the same name and lang_id!'))
        new_document = Document(name=cleaned_data['name'], filename=cleaned_data['filename'],
                                original_filename=cleaned_data['original_filename'],
                                description=cleaned_data['description'])
        new_document.lang = existing_lang
        db.session.add(new_document)
        db.session.commit()
        return new_document

    def read(self, item_id):
        existing_document = Document.query.filter(Document.id == item_id).first()
        if not existing_document:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Document, item_id))
        return existing_document

    def update(self, item_id, input_data):
        existing_document = self.read(item_id)
        cleaned_data = self.parse_input_data(input_data)
        existing_lang = self.lang_api.read(cleaned_data['lang_id'])
        existing_document = self.update_simple_attributes(existing_document, self.simple_params, cleaned_data,
                                                          to_skip=['lang_id', 'filename', 'original_filename'])
        existing_document.lang = existing_lang
        db.session.commit()
        return existing_document

    def delete(self, item_id):
        existing_document = self.read(item_id)
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

    def set_filenames(self, item_id, filename=None, original_filename=None):
        """
        Update the filename and original_filename attributes
        :param item_id:
        :param filename:
        :param original_filename:
        :return:
        """
        existing_document = self.read(item_id)
        if filename:
            existing_document.filename = filename
        if original_filename:
            existing_document.original_filename = original_filename
        db.session.commit()
        return existing_document

    def by_filename(self, filename):
        """
        Return all items that have filename set to @param filename
        :param filename:
        :return:
        """
        all_documents = Document.query.filter(Document.filename == filename).all()
        return all_documents

    def by_lang(self, language):
        lang_api = LangApi()
        db_lang = lang_api.by_lang(language)
        all_documents = Document.query.filter(Document.lang_id == db_lang.id).all()
        return all_documents
