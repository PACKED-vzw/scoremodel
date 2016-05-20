import json

from flask import request, make_response
from flask.ext.login import login_required, current_user

from scoremodel import app
from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.score import ScoreApi
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.modules.msg.messages import public_api_msg, public_error_msg
from scoremodel.modules.user.authentication import must_be_admin


##
# TODO auth so that user_id == user.id for user_report stuff
##


@app.route('/api/report/<int:report_id>', methods=['PUT', 'DELETE'])
@app.route('/api/report', methods=['POST'])
@login_required
@must_be_admin
def a_report(report_id=None):
    a_api = ScoremodelRestApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@app.route('/api/report', methods=['GET'])
@app.route('/api/report/<int:report_id>', methods=['GET'])
def a_report_list(report_id=None):
    a_api = ScoremodelRestApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@app.route('/api/report/<int:report_id>/section/<int:section_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section', methods=['POST'])
@app.route('/api/section/<int:section_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/section', methods=['POST'])
@login_required
@must_be_admin
def a_section(report_id=None, section_id=None):
    a_api = ScoremodelRestApi(api_class=SectionApi, o_request=request, api_obj_id=section_id)
    return a_api.response


@app.route('/api/report/<report_id>/section/<int:section_id>/question/<int:question_id>',
           methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section/<int:section_id>/question', methods=['POST'])
@app.route('/api/question/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/question', methods=['POST'])
@login_required
@must_be_admin
def a_question(report_id=None, section_id=None, question_id=None):
    a_api = ScoremodelRestApi(api_class=QuestionApi, o_request=request, api_obj_id=question_id)
    return a_api.response


@app.route('/api/answer', methods=['GET'])
@login_required
@must_be_admin
def a_answer_list():
    a_api = ScoremodelRestApi(api_class=AnswerApi, o_request=request)
    return a_api.response


@app.route('/api/answer/<int:answer_id>', methods=['GET'])
@login_required
@must_be_admin
def a_answer(answer_id):
    a_api = ScoremodelRestApi(api_class=AnswerApi, o_request=request, api_obj_id=answer_id)
    return a_api.response


@app.route('/api/risk_factor', methods=['GET'])
@login_required
@must_be_admin
def a_risk_factor_list():
    a_api = ScoremodelRestApi(api_class=RiskFactorApi, o_request=request)
    return a_api.response


@app.route('/api/risk_factor/<int:risk_factor_id>')
@login_required
@must_be_admin
def a_risk_factor(risk_factor_id):
    a_api = ScoremodelRestApi(api_class=RiskFactorApi, o_request=request, api_obj_id=risk_factor_id)
    return a_api.response


@app.route('/api/user_report/question_answer/<int:question_answer_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/user_report/question_answer', methods=['POST'])
@login_required
def a_question_answer(question_answer_id=None):
    """
    For POST and PUT requests, we perform the API calls ourselves so we can inject current_user.id
    into input_data. We could request the contents of the request.get_data(), but we don't trust
    that value.
    :param question_answer_id:
    :return:
    """
    response = make_response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'POST':
        question_answer_api = QuestionAnswerApi()
        try:
            input_data = json.loads(request.get_data().decode('utf-8'))
        except ValueError as e:
            response.status_code = 400
            response.data = json.dumps({'msg': u'A JSON error occurred: {0}'.format(e)})
            return response
        input_data['user_id'] = current_user.id
        try:
            created_object = question_answer_api.create(input_data)
        except Exception as e:
            response.status_code = 400
            response.data = json.dumps({'msg': public_error_msg['error_occurred'].format(e)})
            return response

        response.data = json.dumps({'msg': public_api_msg['item_created'].format(question_answer_api, created_object.id),
                                    'data': created_object.output_obj()})
        response.status_code = 200
        return response
    elif request.method == 'PUT':
        question_answer_api = QuestionAnswerApi()
        try:
            input_data = json.loads(request.get_data().decode('utf-8'))
        except ValueError as e:
            response.status_code = 400
            response.data = json.dumps({'msg': u'A JSON error occurred: {0}'.format(e)})
            return response
        input_data['user_id'] = current_user.id
        try:
            created_object = question_answer_api.update(question_answer_id, input_data)
        except Exception as e:
            response.status_code = 400
            response.data = json.dumps({'msg': public_error_msg['error_occurred'].format(e)})
            return response

        response.data = json.dumps({'msg': public_api_msg['item_updated'].format(question_answer_api, created_object.id),
                                    'data': created_object.output_obj()})
        response.status_code = 200
        return response
    else:
        a_api = ScoremodelRestApi(api_class=QuestionAnswerApi, o_request=request, api_obj_id=question_answer_id)
        return a_api.response


@app.route('/api/user_report/<int:user_report_id>/question/<int:question_id>', methods=['GET'])
@login_required
def a_question_public(user_report_id, question_id):
    """
    Get the answers to a specific question
    :param user_report_id:
    :param question_id:
    :return:
    """
    question_answer_api = QuestionAnswerApi()
    response = make_response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    try:
        question_answer = question_answer_api.get_answer_by_question_id(question_id, current_user.id, user_report_id)
    except DatabaseItemDoesNotExist as e:
        response.status_code = 404
        response.data = json.dumps({'msg': public_error_msg['item_not_exists'].format('QuestionAnswer', question_id)})
        return response
    except Exception as e:
        response.status_code = 400
        response.data = json.dumps({'msg': public_error_msg['error_occurred'].format(e)})
        return response
    response.status_code = 200
    response.data = json.dumps({'msg': public_api_msg['items_found'].format('QuestionAnswer'),
                                'data': question_answer.output_obj()})
    return response


@app.route('/api/user_report/<int:user_report_id>', methods=['GET'])
@login_required
def a_user_report(user_report_id):
    """
    For the entire report, get all sections.
    For every section, get all questions that have been answered.
    For every question, get the score.
    For every section, get the score.
    For the report, get the score.
    :param user_report_id:
    :return:
    """
    user_report_api = UserReportApi()
    user_report = user_report_api.read(user_report_id)
    answered_questions = {}
    for section in user_report.template.sections:
        answered_questions[section.id] = {
            'answered_questions': {}
        }
            #get_answer_by_question_id(self, question_id, user_id, user_report_id)
            #get_for_section_by_question_id(self, section_id, user_id, user_report_id)
        question_answer_api = QuestionAnswerApi()
        answered_questions[section.id]['answered_questions'] = question_answer_api.get_for_section_by_question_id\
            (section.id, current_user.id, user_report_id)


@app.route('/api/user_report/<int:user_report_id>/section/<int:section_id>/score', methods=['GET'])
@login_required
def a_section_score_current(user_report_id, section_id):
    """
    Compute the score for the section section_id in user_report user_report_id
    as it stands now - with the questions that are currently answered.
    :param user_report_id:
    :param section_id:
    :return:
    """
    score_api = ScoreApi()
    return score_api.section(user_report_id, section_id)
