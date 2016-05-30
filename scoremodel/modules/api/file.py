from os.path import splitext, join, isfile
from os import getcwd, remove
from flask.ext.babel import gettext as _
from werkzeug.utils import secure_filename
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.error import FileTypeNotAllowed, FileDoesNotExist
from scoremodel import app


class FileApi(GenericApi):

    def create(self, input_file):
        if not self.allowed(input_file.filename):
            raise FileTypeNotAllowed(_('Illegal file type provided.'))
        storage_filename = secure_filename(input_file.filename)
        input_file.save(join(app.config['UPLOAD_FULL_PATH'], storage_filename))
        return {
            'original_filename': input_file.filename,
            'filename': storage_filename
        }

    def read(self, input_filename):
        storage_filename = secure_filename(input_filename)
        if not isfile(join(app.config['UPLOAD_FULL_PATH'], storage_filename)):
            raise FileDoesNotExist(_('No file called {0}.').format(storage_filename))
        return {
            'filename': storage_filename
        }

    def update(self, input_filename, input_file):
        if not self.allowed(input_file.filename):
            raise FileTypeNotAllowed(_('Illegal file type provided.'))
        storage_filename = secure_filename(input_filename)
        input_file.save(join(app.config['UPLOAD_FULL_PATH'], storage_filename))
        return {
            'original_filename': input_file.filename,
            'filename': storage_filename
        }

    def delete(self, input_filename):
        storage_filename = secure_filename(input_filename)
        if not isfile(join(app.config['UPLOAD_FULL_PATH'], storage_filename)):
            raise FileDoesNotExist(_('No file called {0}.').format(storage_filename))
        remove(join(app.config['UPLOAD_FULL_PATH'], storage_filename))
        return True

    def list(self):
        # NOT IMPLEMENTED
        return ()

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
