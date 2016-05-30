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

    def post(self, input_data, additional_opts=None):
        if not additional_opts:
            raise RequiredAttributeMissing(public_error_msg['missing_argument'].format('input_tag_name'))
        input_tag_name = additional_opts['input_tag_name']
        try:
            created_object = self.api.create(self.request.files[input_tag_name])
        except FileTypeNotAllowed as e:
            self.msg = _('Illegal file type.')
            self.status_code = 400
            created_object = None
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            created_object = None
        else:
            self.msg = public_api_msg['item_created'].format(self.api, created_object.filename)
        if created_object is not None:
            return created_object
        else:
            return u''

    def put(self, item_id, input_data, additional_opts=None):
        if not additional_opts:
            raise RequiredAttributeMissing(public_error_msg['missing_argument'].format('input_file'))
        input_tag_name = additional_opts['input_tag_name']
        try:
            updated_object = self.api.update(item_id, self.request.files[input_tag_name])
        except FileTypeNotAllowed as e:
            self.msg = _('Illegal file type.')
            self.status_code = 400
            updated_object = None
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            updated_object = None
        else:
            self.msg = public_api_msg['item_updated'].format(self.api, updated_object.filename)
        if updated_object is not None:
            return updated_object
        else:
            return u''
