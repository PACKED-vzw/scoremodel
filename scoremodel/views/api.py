from scoremodel import app
from flask import request, make_response
from flask.ext.login import login_required
from scoremodel.modules.user.authentication import must_be_admin
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


@app.route('/api/report/<report_id>/section/<int:section_id>/question/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
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
