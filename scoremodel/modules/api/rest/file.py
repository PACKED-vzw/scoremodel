import json
from os.path import splitext, join
from os import getcwd
from flask.ext.babel import gettext as _
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, \
    IllegalEntityType, FileTypeNotAllowed, FileDoesNotExist
from scoremodel.modules.msg.messages import public_api_msg, public_error_msg
from scoremodel.modules.api.rest import RestApi
from scoremodel.modules.api.file import FileApi
from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from werkzeug.utils import secure_filename
from scoremodel import app


##
# Subclass this from ScoremodelRestApi
#   - recreate put & post to support files
#       -> perform file-related functions and add filename and original_filename to the request.data
#       -> hand this over to self.api()
# https://stackoverflow.com/questions/3938569/how-do-i-upload-a-file-with-metadata-using-a-rest-web-service
##


class FileRestApi(ScoremodelRestApi):
    def __init__(self, api_class, o_request, form_file_field=None, api_obj_id=None, translate=None,
                 additional_opts=None):
        self.api = api_class()
        self.file_api = FileApi()
        self.form_file_field = form_file_field
        self.request = o_request
        self.msg = None
        self.output_data = u''
        self.status_code = 200
        self.api_obj_id = api_obj_id
        # TODO: check for completeness
        self.parse_request(api_obj_id=self.api_obj_id, additional_opts=additional_opts)
        ##
        # Set self.response
        ##
        self.response = self.create_response(self.output_data)

    def parse_post(self, input_data_string, additional_opts=None):
        """
        Parse a POST request
        :param input_data_string:
        :param additional_opts:
        :return:
        """
        self.output_data = self.post(additional_opts=additional_opts)

    def get(self, item_id, input_data=None, additional_opts=None):
        existing_file = None
        if not self.api_obj_id:
            # We do not support .list()
            self.status_code = 400
            self.msg = public_error_msg['missing_argument'].format('item_id')
            return u''
        try:
            linked_db_model = self.api.read(self.api_obj_id)
        except DatabaseItemDoesNotExist as e:
            self.status_code = 404
            self.msg = public_error_msg['item_not_exists'].format(self.api, self.api_obj_id)
        except Exception as e:
            self.status_code = 400
            self.msg = public_error_msg['error_occurred'].format(e)
        else:
            try:
                existing_file = self.file_api.read(linked_db_model.filename)
            except FileDoesNotExist:
                self.status_code = 404
                self.msg = public_error_msg['item_not_exists'].format(self.file_api, linked_db_model.filename)
        if existing_file:
            existing_file['linked_id'] = self.api_obj_id
            return existing_file
        else:
            return u''

    def put(self, item_id, input_data, additional_opts=None):
        self.status_code = 405
        self.msg = public_error_msg['illegal_action'].format('PUT')
        return u''

    def post(self, input_data=None, additional_opts=None):
        created_file = None
        if not self.api_obj_id:
            self.status_code = 400
            self.msg = public_error_msg['missing_argument'].format('item_id')
            return u''
        try:
            linked_db_model = self.api.read(self.api_obj_id)
        except DatabaseItemDoesNotExist as e:
            self.status_code = 404
            self.msg = public_error_msg['item_not_exists'].format(self.api, self.api_obj_id)
        except Exception as e:
            self.status_code = 400
            self.msg = public_error_msg['error_occurred'].format(e)
        else:
            input_file = self.request.files[self.form_file_field]  # TODO check
            if self.linked_db_model_has_attachment(linked_db_model):
                # Consider this an update
                created_file = self.file_api.update(linked_db_model.filename, input_file)
            else:
                # A new creation
                created_file = self.file_api.create(self.request.files[self.form_file_field])

            try:
                self.attach_to_linked_db_model(original_filename=input_file.filename,
                                               filename=created_file['filename'])
            except DatabaseItemDoesNotExist as e:
                self.status_code = 404
                self.msg = public_error_msg['item_not_exists'].format(self.api, self.api_obj_id)
        if created_file is not None:
            created_file['linked_id'] = self.api_obj_id
            return created_file
        else:
            return u''

    def attach_to_linked_db_model(self, original_filename, filename):
        return self.api.set_filenames(self.api_obj_id, filename=filename, original_filename=original_filename)

    def linked_db_model_has_attachment(self, linked_db_model):
        if hasattr(linked_db_model, 'filename') and linked_db_model.filename is not None:
            return True
        return False
