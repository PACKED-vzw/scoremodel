from flask import request
from flask_login import login_required

from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.report.create import ReportCreateApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel import csrf

from scoremodel.views.api import api


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


@csrf.exempt
@api.route('/report', methods=['GET'])
@api.route('/report/<int:report_id>', methods=['GET'])
def v_api_public_report(report_id=None):
    a_api = ScoremodelRestApi(api_class=ReportApi, o_request=request, api_obj_id=report_id)
    return a_api.response


@csrf.exempt
@api.route('/section', methods=['GET'])
@api.route('/section/<int:section_id>', methods=['GET'])
def v_api_public_section(section_id=None):
    ##
    # Add total score
    def hook_add_total_score(output_data):
        if section_id is not None:
            new_output = output_data
            new_output['total_score'] = SectionApi().total_score(section_id)
        else:
            new_output = []
            for item in output_data:
                item['total_score'] = SectionApi().total_score(item['id'])
                new_output.append(item)
        return new_output

    ##
    # Add multiplication factor
    def hook_add_multiplication_factor(output_data):
        if section_id is not None:
            new_output = output_data
            new_output['multiplication_factor'] = SectionApi().multiplication_factor(section_id)
        else:
            new_output = []
            for item in output_data:
                item['multiplication_factor'] = SectionApi().multiplication_factor(item['id'])
                new_output.append(item)
        return new_output

    a_api = ScoremodelRestApi(api_class=SectionApi, o_request=request, api_obj_id=section_id,
                              posthooks=(hook_add_total_score, hook_add_multiplication_factor))
    return a_api.response


@csrf.exempt
@api.route('/question', methods=['GET'])
@api.route('/question/<int:question_id>', methods=['GET'])
def v_api_public_question(question_id=None):
    ##
    # Add maximum score
    def hook_add_maximum_score(output_data):
        if question_id is not None:
            new_output = output_data
            new_output['maximum_score'] = QuestionApi().maximum_score(question_id)
        else:
            new_output = []
            for item in output_data:
                item['maximum_score'] = QuestionApi().maximum_score(item['id'])
                new_output.append(item)
        return new_output

    a_api = ScoremodelRestApi(api_class=QuestionApi, o_request=request, api_obj_id=question_id)
    return a_api.response


@csrf.exempt
@api.route('/answer', methods=['GET'])
@api.route('/answer/<int:answer_id>', methods=['GET'])
def v_api_public_answer(answer_id=None):
    a_api = ScoremodelRestApi(api_class=AnswerApi, o_request=request, api_obj_id=answer_id)
    return a_api.response


@csrf.exempt
@api.route('/risk_factor', methods=['GET'])
@api.route('/risk_factor/<int:risk_factor_id>', methods=['GET'])
def v_api_public_risk_factor(risk_factor_id=None):
    a_api = ScoremodelRestApi(api_class=RiskFactorApi, o_request=request, api_obj_id=risk_factor_id)
    return a_api.response