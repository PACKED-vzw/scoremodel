from flask import make_response, request
import json
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.msg.messages import error_msg


class ScoreApi:
    def __init__(self):
        self.response = make_response()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'

    def section(self, user_report_id, section_id):
        user_report_api = UserReportApi()
        section_api = SectionApi()
        try:
            user_report = user_report_api.read(user_report_id)
        except Exception as e:
            return self.fail(error_code=400, error_message=e)
        try:
            section = section_api.read(section_id)
        except Exception as e:
            return self.fail(error_code=400, error_message=e)
        question_ids = [question.id for question in section.questions]
        current_score = 0
        for question_answer in user_report.question_answers:
            if question_answer.question_id in question_ids:
                current_score = current_score + question_answer.score
        self.response.status_code = 200
        self.response.data = json.dumps({
            'msg': 'Score computed',
            'data': {
                'score': current_score,
                'multiplication_factor': section.multiplication_factor
            }
        })
        return self.response

    def fail(self, error_code=None, error_message=None):
        if error_code:
            self.response.status_code = error_code
        else:
            self.response.status_code = 400
        if error_msg:
            self.response.data = json.dumps({'msg': error_msg['error_occurred'].format(error_message), 'data': None})
        else:
            self.response.data = json.dumps({'msg': error_msg['error_occurred'].format(''), 'data': None})
        return self.response
