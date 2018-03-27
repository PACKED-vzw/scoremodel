from os.path import splitext, join, isfile
from os import getcwd, remove
import mimetypes
from flask_babel import gettext as _
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
            'filename': storage_filename,
            'mimetype': mimetypes.guess_type(storage_filename)[0]
        }

    def read(self, input_filename):
        storage_filename = secure_filename(input_filename)
        if not isfile(join(app.config['UPLOAD_FULL_PATH'], storage_filename)):
            raise FileDoesNotExist(_('No file called {0}.').format(storage_filename))
        return {
            'filename': storage_filename,
            'mimetype': mimetypes.guess_type(storage_filename)[0]
        }

    def update(self, input_filename, input_file):
        if not self.allowed(input_file.filename):
            raise FileTypeNotAllowed(_('Illegal file type provided.'))
        old_storage_filename = secure_filename(input_filename)
        new_storage_filename = secure_filename(input_file.filename)
        # Delete the old storage_filename
        self.delete(old_storage_filename)
        input_file.save(join(app.config['UPLOAD_FULL_PATH'], new_storage_filename))
        return {
            'original_filename': input_file.filename,
            'filename': new_storage_filename,
            'mimetype': mimetypes.guess_type(new_storage_filename)[0]
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

    def by_storage_filename(self, input_filename):
        return self.read(input_filename)

    def allowed(self, filename):
        """
        Check whether the file is of an allowed filetype
        TODO (?) perform check on filesystem?
        :param filename:
        :return:
        """
        extension = splitext(filename)[1]
        # The first char of extension is the dot, so we remove it using slicing
        if extension[1:].lower() in app.config['ALLOWED_EXTENSIONS']:
            return True
        return False
