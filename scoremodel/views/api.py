from scoremodel import app
from flask import request, make_response
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api import ScoremodelApi
from scoremodel.modules.error import IDMissingForCUD
from scoremodel.modules.msg.messages import api_msg, error_msg
import json

##
# TODO support auth
# TODO GET risk_factor, GET answer
##


@app.route('/api/report/<int:report_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report', methods=['POST'])
def a_report(report_id=None):
    a_api = ScoremodelApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@app.route('/api/report/<int:report_id>/section/<int:section_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section', methods=['POST'])
@app.route('/api/section/<int:section_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/section', methods=['POST'])
def a_section(report_id=None, section_id=None):
    a_api = ScoremodelApi(api_class=SectionApi, o_request=request, api_obj_id=section_id)
    return a_api.response


@app.route('/api/report/<report_id>/section/<int:section_id>/question/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section/<int:section_id>/question', methods=['POST'])
@app.route('/api/question/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/question', methods=['POST'])
def a_question(report_id=None, section_id=None, question_id=None):
    a_api = ScoremodelApi(api_class=QuestionApi, o_request=request, api_obj_id=question_id)
    return a_api.response


@app.route('/api/answer', methods=['GET'])
def a_answer_list():
    a_api = AnswerApi()
    answer_list = a_api.list()
    output_list = []
    for answer in answer_list:
        output_list.append(answer.output_obj())
    resp = make_response()
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.data = json.dumps({
        'msg': '',
        'data': output_list
    })
    return resp


@app.route('/api/answer/<int:answer_id>', methods=['GET'])
def a_answer(answer_id):
    a_api = ScoremodelApi(api_class=AnswerApi, o_request=request, api_obj_id=answer_id)
    return a_api.response


@app.route('/api/risk_factor', methods=['GET'])
def a_risk_factor_list():
    a_api = RiskFactorApi()
    risk_factors_list = a_api.list()
    output_list = []
    for risk_factor in risk_factors_list:
        output_list.append(risk_factor.output_obj())
    resp = make_response()
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.data = json.dumps({
        'msg': '',
        'data': output_list
    })
    return resp


@app.route('/api/risk_factor/<int:risk_factor_id>')
def a_risk_factor(risk_factor_id):
    a_api = ScoremodelApi(api_class=RiskFactorApi, o_request=request, api_obj_id=risk_factor_id)
    return a_api.response
