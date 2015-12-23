from scoremodel import app
from flask import request, make_response
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.error import IDMissingForCUD
import json


@app.route('/api/report/<int:report_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report', methods=['POST'])
def a_report(report_id=None):
    api_report = ReportApi()
    resp = make_response()
    if request.method == 'GET':
        o_report = api_report.read(report_id)
        resp.data = json.dumps(o_report.output_obj())
    elif request.method == 'DELETE':
        response = {
            'msg': 'Report {0} deleted'.format(report_id),
            'is_deleted': api_report.delete(report_id)
        }
        resp.data = json.dumps(response)
    else:
        input_data_raw = request.get_data()
        input_data_dict = json.loads(input_data_raw.decode('utf-8'))
        if request.method == 'POST':
            o_report = api_report.create(input_data_dict)
            response = {
                'msg': 'New report created',
                'report': o_report.output_obj()
            }
            resp.data = json.dumps(response)
        if request.method == 'PUT':
            o_report = api_report.update(report_id, input_data_dict)
            response = {
                'msg': 'Report {0} updated'.format(report_id),
                'report': o_report.output_obj()
            }
            resp.data = json.dumps(response)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/api/report/<int:report_id>/section/<int:section_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section', methods=['POST'])
def a_section(report_id, section_id=None):
    pass


@app.route('/api/report/<report_id>/section/<int:section_id>/question/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/report/<int:report_id>/section/<int:section_id>/question', methods=['POST'])
def a_question(report_id, section_id, question_id=None):
    pass
