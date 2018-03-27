from flask import request, make_response, send_from_directory
from flask_login import login_required
from flask_babel import gettext as _

from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.api.rest.file import FileRestApi
from scoremodel.modules.api.file import FileApi
from scoremodel.modules.api.page import PageApi
from scoremodel.modules.api.document import DocumentApi
from scoremodel.modules.error import DatabaseItemDoesNotExist, RequiredAttributeMissing, FileDoesNotExist
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel import app, csrf
from scoremodel.views.api import api


@api.route('/page', methods=['POST'])
@api.route('/page/<int:page_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_page(page_id=None):
    def hook_check_lang_id_and_menu_link_id(input_data):
        if not page_id:
            # It is a .create()
            return input_data
        parsed_data = input_data
        page_api = PageApi()
        current_page = page_api.read(page_id)
        if 'lang_id' not in parsed_data or 'menu_link_id' not in parsed_data:
            # All failures should be handled by ScoremodelRestApi
            return input_data
        if current_page.lang_id != parsed_data['lang_id']:
            raise RequiredAttributeMissing(_('You cannot update lang_id!'))
        if current_page.menu_link_id != parsed_data['menu_link_id']:
            raise RequiredAttributeMissing(_('You cannot update menu_link_id!'))
        return input_data

    a_api = ScoremodelRestApi(api_class=PageApi, o_request=request, api_obj_id=page_id,
                              hooks=[hook_check_lang_id_and_menu_link_id])
    return a_api.response


@csrf.exempt
@api.route('/page', methods=['GET'])
@api.route('/page/<int:page_id>', methods=['GET'])
def v_api_public_page(page_id=None):
    a_api = ScoremodelRestApi(api_class=PageApi, o_request=request, api_obj_id=page_id)
    return a_api.response


@api.route('/document', methods=['POST'])
@login_required
@must_be_admin
def v_api_document_create():
    a_api = ScoremodelRestApi(api_class=DocumentApi, o_request=request)
    return a_api.response


@api.route('/document/<int:document_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
# Forbid updating the document filename
def v_api_document_edit(document_id):
    def hook_check_filename(input_data):
        parsed_data = input_data
        document_api = DocumentApi()
        try:
            existing_document = document_api.read(document_id)
        except Exception as e:
            return input_data
        if 'original_filename' not in parsed_data:
            return input_data
        if parsed_data['original_filename'] != existing_document.original_filename:
            raise RequiredAttributeMissing(_('You cannot modify original_filename!'))
        if 'filename' in parsed_data and parsed_data['filename'] != existing_document.filename:
            raise RequiredAttributeMissing(_('You cannot modify filename!'))
        return input_data

    a_api = ScoremodelRestApi(api_class=DocumentApi, o_request=request, api_obj_id=document_id,
                              hooks=[hook_check_filename])
    return a_api.response


@csrf.exempt
@api.route('/document/<int:document_id>/resource', methods=['POST'])
@login_required
@must_be_admin
def v_api_document_resource_upload(document_id):
    a_api = FileRestApi(api_class=DocumentApi, o_request=request, form_file_field='input_file', api_obj_id=document_id)
    return a_api.response


@csrf.exempt
@api.route('/document/<int:document_id>/resource', methods=['GET'])
def v_api_document_resource(document_id):
    file_api = FileApi()
    document_api = DocumentApi()
    try:
        existing_document = document_api.read(document_id)
    except DatabaseItemDoesNotExist as e:
        response = make_response()
        response.status_code = 404
        return response
    except Exception as e:
        response = make_response()
        response.status_code = 400
        return response
    try:
        existing_file = file_api.read(existing_document.filename)
    except FileDoesNotExist as e:
        response = make_response()
        response.status_code = 404
        return response
    return send_from_directory(app.config['UPLOAD_FULL_PATH'], existing_file['filename'])


@csrf.exempt
@api.route('/resource/<string:resource_name>', methods=['GET'])
def v_api_resource(resource_name):
    file_api = FileApi()
    try:
        existing_file = file_api.by_storage_filename(resource_name)
    except FileDoesNotExist as e:
        response = make_response()
        response.status_code = 404
        return response
    return send_from_directory(app.config['UPLOAD_FULL_PATH'], existing_file['filename'])


@csrf.exempt
@api.route('/document/<int:document_id>', methods=['GET'])
@api.route('/document')
def v_api_document(document_id=None):
    a_api = ScoremodelRestApi(api_class=DocumentApi, o_request=request, api_obj_id=document_id)
    return a_api.response