import json

from flask import request
from flask.ext.login import login_required, current_user

from scoremodel import app
from scoremodel.modules.api import ScoremodelApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.msg.messages import api_msg, error_msg
from scoremodel.modules.user.authentication import must_be_admin


##
# TODO support auth
# TODO GET risk_factor, GET answer
##


@app.route('/api/report/<int:report_id>', methods=['PUT', 'DELETE'])
@app.route('/api/report', methods=['POST'])
@login_required
@must_be_admin
def a_report(report_id=None):
    a_api = ScoremodelApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@app.route('/api/report', methods=['GET'])
@app.route('/api/report/<int:report_id>', methods=['GET'])
def a_report_list(report_id=None):
    a_api = ScoremodelApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@app.route('/api/report/<int:report_id>/section/<int:section_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section', methods=['POST'])
@app.route('/api/section/<int:section_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/section', methods=['POST'])
@login_required
@must_be_admin
def a_section(report_id=None, section_id=None):
    a_api = ScoremodelApi(api_class=SectionApi, o_request=request, api_obj_id=section_id)
    return a_api.response


@app.route('/api/report/<report_id>/section/<int:section_id>/question/<int:question_id>',
           methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section/<int:section_id>/question', methods=['POST'])
@app.route('/api/question/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/question', methods=['POST'])
@login_required
@must_be_admin
def a_question(report_id=None, section_id=None, question_id=None):
    a_api = ScoremodelApi(api_class=QuestionApi, o_request=request, api_obj_id=question_id)
    return a_api.response


@app.route('/api/answer', methods=['GET'])
@login_required
@must_be_admin
def a_answer_list():
    a_api = ScoremodelApi(api_class=AnswerApi, o_request=request)
    return a_api.response


@app.route('/api/answer/<int:answer_id>', methods=['GET'])
@login_required
@must_be_admin
def a_answer(answer_id):
    a_api = ScoremodelApi(api_class=AnswerApi, o_request=request, api_obj_id=answer_id)
    return a_api.response


@app.route('/api/risk_factor', methods=['GET'])
@login_required
@must_be_admin
def a_risk_factor_list():
    a_api = ScoremodelApi(api_class=RiskFactorApi, o_request=request)
    return a_api.response


@app.route('/api/risk_factor/<int:risk_factor_id>')
@login_required
@must_be_admin
def a_risk_factor(risk_factor_id):
    a_api = ScoremodelApi(api_class=RiskFactorApi, o_request=request, api_obj_id=risk_factor_id)
    return a_api.response


@app.route('/api/user_report/question_answer/<int:question_answer_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/user_report/question_answer', methods=['POST'])
@login_required
def a_question_answer(question_answer_id):
    """
    For POST and PUT requests, we perform the API calls ourselves so we can inject current_user.id
    into input_data. We could request the contents of the request.get_data(), but we don't trust
    that value.
    :param question_answer_id:
    :return:
    """
    if request.method == 'POST':
        question_answer_api = QuestionAnswerApi()
        try:
            input_data = json.loads(request.get_data().decode('utf-8'))
        except ValueError as e:
            return json.dumps({'msg': u'A JSON error occurred: {0}'.format(e)}), 400
        input_data['user_id'] = current_user.id
        try:
            created_object = question_answer_api.create(input_data)
        except Exception as e:
            return json.dumps({'msg': error_msg['error_occurred'].format(e)}), 400
        return json.dumps({'msg': api_msg['item_created'].format(question_answer_api, created_object.id),
                           'data': created_object.output_obj()})
    elif request.method == 'PUT':
        question_answer_api = QuestionAnswerApi()
        try:
            input_data = json.loads(request.get_data().decode('utf-8'))
        except ValueError as e:
            return json.dumps({'msg': u'A JSON error occurred: {0}'.format(e)}), 400
        input_data['user_id'] = current_user.id
        try:
            created_object = question_answer_api.update(question_answer_id, input_data)
        except Exception as e:
            return json.dumps({'msg': error_msg['error_occurred'].format(e)}), 400
        return json.dumps({'msg': api_msg['item_updated'].format(question_answer_api, created_object.id),
                           'data': created_object.output_obj()})
    else:
        a_api = ScoremodelApi(api_class=QuestionAnswerApi, o_request=request, api_obj_id=question_answer_id)
        return a_api.response


@app.route('/api/user_report/question/<int:question_id>', methods=['GET'])
@login_required
def a_question_public(question_id):
    a_api = ScoremodelApi(api_class=QuestionApi, o_request=request, api_obj_id=question_id)
    return a_api.response
