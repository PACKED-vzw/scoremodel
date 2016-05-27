import json
from os.path import splitext, join
from os import getcwd
from flask.ext.babel import gettext as _
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, \
    IllegalEntityType
from scoremodel.modules.msg.messages import public_api_msg, public_error_msg
from scoremodel.modules.api.rest import RestApi
from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from werkzeug.utils import secure_filename
from scoremodel import app

##
# Subclass this from ScoremodelRestApi
#   - recreate put & post to support files
#       -> perform file-related functions and add filename and original_filename to the request.data
#       -> hand this over to self.api()
##


class FileApi(ScoremodelRestApi):

    def __init__(self, api_class, o_request, input_tag_name, hooks=(), api_obj_id=None):
        """
        :param api_class:
        :param o_request:
        :param input_tag_name: the name of the <input field that contains the file.
        :param hooks:
        """
        self.api = api_class()
        self.request = o_request
        self.input_tag_name = input_tag_name
        self.msg = None
        self.output_data = u''
        self.status_code = 200
        ##
        # Perform the hooks
        # If a hook fails, we error out immediately
        ##
        try:
            for hook in hooks:
                input_data_string = hook(input_data_string)
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
        else:
            ##
            # Parse the original request and execute the correct self.action() for the request.method
            ##
            pass
        ##
        # Set self.response
        ##
        self.response = self.create_response(self.output_data)

    def post(self):
        """
        This class only deals with uploading files
        :return:
        """
        if self.input_tag_name not in self.request.files:
            self.msg = _('Error: file not found.')
            self.status_code = 400
            return u''
        input_file = self.request.files[self.input_tag_name]
        if not self.allowed(input_file.name):
            self.msg = _('File type not allowed.')
            self.status_code = 400
            return u''
        storage_filename = secure_filename(input_file.name)
        input_file.save(join(getcwd(), app.config['UPLOAD_FOLDER'], storage_filename))
        self.msg = _('File uploaded.')
        ##
        # New files must be registered in the DB
        ##
        return self.api.create({
            'filename': storage_filename,
            'original_filename': input_file.name
        })

    def put(self, api_obj_id):
        pass

    def create_response(self, data):
        """
        Create an API response
        :param data:
        :return:
        """
        rest_api = RestApi()
        return rest_api.response(status=self.status_code, data=data, msg=self.msg)

    def allowed(self, filename):
        """
        Check whether the file is of an allowed filetype
        TODO (?) perform check on filesystem?
        :param filename:
        :return:
        """
        if splitext(filename)[1] in app.config['ALLOWED_EXTENSIONS']:
            return True
        return False
