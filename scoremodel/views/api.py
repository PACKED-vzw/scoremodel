from scoremodel import app
from flask import request, make_response
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
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
