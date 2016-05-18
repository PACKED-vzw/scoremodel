import json

from flask import request, make_response
from flask.ext.login import login_required, current_user
from flask import Blueprint, render_template

from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.api.question_answer.rest_api import QuestionAnswerQueryRestApi, QuestionAnswerQuestionQueryRestApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.score import ScoreApi
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.modules.msg.messages import api_msg, error_msg
from scoremodel.modules.user.authentication import must_be_admin

api = Blueprint('api', __name__, url_prefix='/api/v2')


@api.route('/report', methods=['POST'])
@api.route('/report/<int:report_id>', methods=['PUT', 'DELETE'])
@login_required
@must_be_admin
def v_api_report(report_id=None):
    a_api = ScoremodelRestApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
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

