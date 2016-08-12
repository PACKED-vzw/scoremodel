import json

from flask import request, make_response, send_from_directory, abort
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _
from flask import Blueprint, render_template

from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.api.rest.file import FileRestApi
from scoremodel.modules.api.rest import RestApi
from scoremodel.modules.api.file import FileApi
from scoremodel.modules.api.question_answer.rest_api import QuestionAnswerQueryRestApi, QuestionAnswerQuestionQueryRestApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.report.create import ReportCreateApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.page import PageApi
from scoremodel.modules.api.document import DocumentApi
from scoremodel.modules.locale import Locale
from scoremodel.modules.error import DatabaseItemDoesNotExist, RequiredAttributeMissing, FileDoesNotExist
from scoremodel.modules.msg.messages import public_api_msg, public_error_msg
from scoremodel.modules.user.authentication import must_be_admin, requires_auth
from scoremodel import db, app

api = Blueprint('api', __name__, url_prefix='/api/v2')


@api.route('/report', methods=['POST'])
@api.route('/report/<int:report_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_report(report_id=None):
    a_api = ScoremodelRestApi(api_class=ReportCreateApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@api.route('/section', methods=['POST'])
@api.route('/section/<int:section_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_section(section_id=None):
    a_api = ScoremodelRestApi(api_class=SectionApi, o_request=request, api_obj_id=section_id)
    return a_api.response


@api.route('/question', methods=['POST'])
@api.route('/question/<int:question_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_question(question_id=None):
    a_api = ScoremodelRestApi(api_class=QuestionApi, o_request=request, api_obj_id=question_id)
    return a_api.response


@api.route('/answer', methods=['POST'])
@api.route('/answer/<int:answer_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_answer(answer_id=None):
    a_api = ScoremodelRestApi(api_class=AnswerApi, o_request=request, api_obj_id=answer_id)
    return a_api.response


@api.route('/risk_factor', methods=['POST'])
@api.route('/risk_factor/<int:risk_factor_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_risk_factor(risk_factor_id=None):
    a_api = ScoremodelRestApi(api_class=RiskFactorApi, o_request=request, api_obj_id=risk_factor_id)
    return a_api.response


@api.route('/benchmark', methods=['POST'])
@api.route('/benchmark/<int:benchmark_report_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_benchmark(benchmark_report_id=None):
    pass


@api.route('/report', methods=['GET'])
@api.route('/report/<int:report_id>', methods=['GET'])
def v_api_public_report(report_id=None):
    a_api = ScoremodelRestApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@api.route('/section', methods=['GET'])
@api.route('/section/<int:section_id>', methods=['GET'])
def v_api_public_section(section_id=None):
    a_api = ScoremodelRestApi(api_class=SectionApi, o_request=request, api_obj_id=section_id)
    return a_api.response


@api.route('/question', methods=['GET'])
@api.route('/question/<int:question_id>', methods=['GET'])
def v_api_public_question(question_id=None):
    a_api = ScoremodelRestApi(api_class=QuestionApi, o_request=request, api_obj_id=question_id)
    return a_api.response


@api.route('/answer', methods=['GET'])
@api.route('/answer/<int:answer_id>', methods=['GET'])
def v_api_public_answer(answer_id=None):
    a_api = ScoremodelRestApi(api_class=AnswerApi, o_request=request, api_obj_id=answer_id)
    return a_api.response


@api.route('/risk_factor', methods=['GET'])
@api.route('/risk_factor/<int:risk_factor_id>', methods=['GET'])
def v_api_public_risk_factor(risk_factor_id=None):
    a_api = ScoremodelRestApi(api_class=RiskFactorApi, o_request=request, api_obj_id=risk_factor_id)
    return a_api.response


@api.route('/question_answer', methods=['GET', 'POST'])
@api.route('/question_answer/<int:question_answer_id>', methods=['PUT', 'DELETE', 'GET'])
@login_required
def v_api_question_answer(question_answer_id=None):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        try:
            parsed_data = json.loads(input_data)
        except ValueError as e:
            # If parsing the data as JSON fails, return to ScoremodelApi so
            # it can handle the failure gracefully.
            return input_data
        parsed_data['user_id'] = current_user.id
        return json.dumps(parsed_data)
    a_api = ScoremodelRestApi(api_class=QuestionAnswerApi, o_request=request, api_obj_id=question_answer_id,
                              hooks=[hook_insert_current_user])
    return a_api.response


@api.route('/benchmark', methods=['GET'])
@api.route('/benchmark/<int:benchmark_report_id>', methods=['GET'])
def v_api_public_benchmark(benchmark_report_id=None):
    pass


##
# Create a API call that, given user_report, answer_id, question_id, either:
# returns the question_answer if it exists
# updates the new question_answer if user_report, question_id exists but answer_id != our_answer_id
# creates a new question_answer if none exists
##
@api.route('/user_report/<int:user_report_id>/question/<int:question_id>/answer/<int:answer_id>',
           methods=['GET', 'POST'])
@login_required
def v_api_create_question_answer(user_report_id, question_id, answer_id):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        if input_data:
            try:
                parsed_data = json.loads(input_data)
            except ValueError as e:
                # If parsing the data as JSON fails, return to ScoremodelApi so
                # it can handle the failure gracefully.
                return input_data
        else:
            parsed_data = {}
        parsed_data['user_id'] = current_user.id
        return json.dumps(parsed_data)

    # Create a hook to insert user_report_id, question_id and answer_id into input_data
    def hook_insert_ids(input_data):
        if input_data:
            try:
                parsed_data = json.loads(input_data)
            except ValueError as e:
                # If parsing the data as JSON fails, return to ScoremodelApi so
                # it can handle the failure gracefully.
                return input_data
        else:
            parsed_data = {}
        parsed_data['user_report_id'] = user_report_id
        parsed_data['question_id'] = question_id
        parsed_data['answer_id'] = answer_id
        return json.dumps(parsed_data)

    # api_obj_id can not be None, but it is ignored in this case
    a_api = QuestionAnswerQueryRestApi(api_class=QuestionAnswerApi, o_request=request, api_obj_id='',
                                       hooks=[hook_insert_current_user, hook_insert_ids])
    return a_api.response


@api.route('/user_report/<int:user_report_id>/question/<int:question_id>', methods=['GET'])
@login_required
def v_api_get_question_answer(user_report_id, question_id):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        if input_data:
            try:
                parsed_data = json.loads(input_data)
            except ValueError as e:
                # If parsing the data as JSON fails, return to ScoremodelApi so
                # it can handle the failure gracefully.
                return input_data
        else:
            parsed_data = {}
        parsed_data['user_id'] = current_user.id
        return json.dumps(parsed_data)

    # Create a hook to insert user_report_id, question_id and answer_id into input_data
    def hook_insert_ids(input_data):
        if input_data:
            try:
                parsed_data = json.loads(input_data)
            except ValueError as e:
                # If parsing the data as JSON fails, return to ScoremodelApi so
                # it can handle the failure gracefully.
                return input_data
        else:
            parsed_data = {}
        parsed_data['user_report_id'] = user_report_id
        parsed_data['question_id'] = question_id
        return json.dumps(parsed_data)

    # api_obj_id can not be None, but it is ignored in this case
    a_api = QuestionAnswerQuestionQueryRestApi(api_class=QuestionAnswerApi, o_request=request, api_obj_id='',
                                               hooks=[hook_insert_current_user, hook_insert_ids])
    return a_api.response


@api.route('/user_report', methods=['GET', 'POST'])
@api.route('/user_report/<int:user_report_id>', methods=['PUT', 'DELETE', 'GET'])
@login_required
def v_api_user_report(user_report_id=None):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        try:
            parsed_data = json.loads(input_data)
        except ValueError as e:
            # If parsing the data as JSON fails, return to ScoremodelApi so
            # it can handle the failure gracefully.
            return input_data
        parsed_data['user_id'] = current_user.id
        return json.dumps(parsed_data)

    a_api = ScoremodelRestApi(api_class=UserReportApi, o_request=request, api_obj_id=user_report_id,
                              hooks=[hook_insert_current_user])
    return a_api.response


@api.route('/page', methods=['POST'])
@api.route('/page/<int:page_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_page(page_id=None):
    def hook_check_lang_id_and_menu_link_id(input_data):
        if not page_id:
            # It is a .create()
            return input_data
        try:
            parsed_data = json.loads(input_data)
        except ValueError as e:
            return input_data
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
        try:
            parsed_data = json.loads(input_data)
        except ValueError as e:
            return input_data
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


@api.route('/document/<int:document_id>/resource', methods=['POST'])
@login_required
@must_be_admin
def v_api_document_resource_upload(document_id):
    a_api = FileRestApi(api_class=DocumentApi, o_request=request, form_file_field='input_file', api_obj_id=document_id)
    return a_api.response


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


@api.route('/document/<int:document_id>', methods=['GET'])
@api.route('/document')
def v_api_document(document_id=None):
    a_api = ScoremodelRestApi(api_class=DocumentApi, o_request=request, api_obj_id=document_id)
    return a_api.response


@api.route('/locale/<string:locale_name>', methods=['POST'])
@api.route('/locale', methods=['GET'])
def v_set_locale(locale_name=None):
    locale_api = Locale()
    rest_api = RestApi()
    data = u''
    if not locale_name:
        status_code = 200
        data = json.dumps({'locale': locale_api.current_locale})
    else:
        if locale_api.set_locale(locale_name) is True:
            status_code = 200
        else:
            status_code = 400
    return rest_api.response(status=status_code, data=data)
