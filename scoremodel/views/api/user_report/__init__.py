from flask import request
from flask_login import login_required, current_user

from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.api.question_answer.rest_api import QuestionAnswerQueryRestApi,\
    QuestionAnswerQuestionQueryRestApi
from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel import csrf

from scoremodel.views.api import api


@api.route('/question_answer', methods=['GET', 'POST'])
@api.route('/question_answer/<int:question_answer_id>', methods=['PUT', 'DELETE', 'GET'])
@login_required
def v_api_question_answer(question_answer_id=None):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        input_data['user_id'] = current_user.id
        return input_data
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
            parsed_data = input_data
        else:
            parsed_data = {}
        parsed_data['user_id'] = current_user.id
        return parsed_data

    # Create a hook to insert user_report_id, question_id and answer_id into input_data
    def hook_insert_ids(input_data):
        if input_data:
            parsed_data  = input_data
        else:
            parsed_data = {}
        parsed_data['user_report_id'] = user_report_id
        parsed_data['question_id'] = question_id
        parsed_data['answer_id'] = answer_id
        return parsed_data

    # api_obj_id can not be None, but it is ignored in this case
    a_api = QuestionAnswerQueryRestApi(api_class=QuestionAnswerApi, o_request=request, api_obj_id='',
                                       hooks=[hook_insert_current_user, hook_insert_ids])
    return a_api.response


@csrf.exempt
@api.route('/user_report/<int:user_report_id>/question/<int:question_id>', methods=['GET'])
@login_required
def v_api_get_question_answer(user_report_id, question_id):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        if input_data:
            parsed_data = input_data
        else:
            parsed_data = {}
        parsed_data['user_id'] = current_user.id
        return parsed_data

    # Create a hook to insert user_report_id, question_id and answer_id into input_data
    def hook_insert_ids(input_data):
        if input_data:
            parsed_data = input_data
        else:
            parsed_data = {}
        parsed_data['user_report_id'] = user_report_id
        parsed_data['question_id'] = question_id
        return parsed_data

    # Insert the multiplication factor
    def hook_add_multiplication_factor(output_data):
        if type(output_data) is not dict:
            return output_data
        question = QuestionApi().read(question_id)
        output_data['multiplication_factor'] = SectionApi().multiplication_factor(question.section_id)
        return output_data

    # api_obj_id can not be None, but it is ignored in this case
    a_api = QuestionAnswerQuestionQueryRestApi(api_class=QuestionAnswerApi, o_request=request, api_obj_id='',
                                               prehooks=(hook_insert_current_user, hook_insert_ids),
                                               posthooks=(hook_add_multiplication_factor,))
    return a_api.response


@csrf.exempt
@api.route('/user_report', methods=['GET'])
@api.route('/user_report/<int:user_report_id>', methods=['GET'])
@login_required
def v_api_user_report_get(user_report_id=None):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        parsed_data = input_data
        parsed_data['user_id'] = current_user.id
        return parsed_data

    # Add the multiplication factor for every question_answer
    def hook_add_multiplication_factor(output_data):
        if type(output_data) is not dict:
            return output_data
        new_question_answers_by_section = []
        for section in output_data['question_answers_by_section']:
            question_answers = []
            for qa in section['question_answers']:
                qa['multiplication_factor'] = SectionApi().multiplication_factor(section['section_id'])
                question_answers.append(qa)
            section['question_answers'] = question_answers
            new_question_answers_by_section.append(section)
        output_data['question_answers_by_section'] = new_question_answers_by_section
        return output_data

    a_api = ScoremodelRestApi(api_class=UserReportApi, o_request=request, api_obj_id=user_report_id,
                              prehooks=(hook_insert_current_user,), posthooks=(hook_add_multiplication_factor,))
    return a_api.response


@api.route('/user_report', methods=['POST'])
@api.route('/user_report/<int:user_report_id>', methods=['PUT', 'DELETE'])
@login_required
def v_api_user_report(user_report_id=None):
    # Create a hook to insert current_user.id in the original data.
    def hook_insert_current_user(input_data):
        parsed_data = input_data
        parsed_data['user_id'] = current_user.id
        return parsed_data

    a_api = ScoremodelRestApi(api_class=UserReportApi, o_request=request, api_obj_id=user_report_id,
                              hooks=[hook_insert_current_user])
    return a_api.response
