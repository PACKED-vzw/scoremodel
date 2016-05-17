from sqlalchemy import and_

from scoremodel import db
from scoremodel.models.general import Section
from scoremodel.models.public import QuestionAnswer
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.error import DatabaseItemAlreadyExists, DatabaseItemDoesNotExist

#TODO: for get, check current_user!

class QuestionAnswerApi(GenericApi):
    simple_params = ['user_id', 'question_id', 'answer_id', 'user_report_id']
    complex_params = []
    required_params = ['user_id', 'question_id', 'answer_id', 'user_report_id']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        new_question_answer = QuestionAnswer(user_id=cleaned_data['user_id'], question_id=cleaned_data['question_id'],
                                             answer_id=cleaned_data['answer_id'],
                                             user_report_id=cleaned_data['user_report_id'])
        db.session.add(new_question_answer)
        db.session.commit()
        return new_question_answer

    def read(self, question_answer_id):
        existing_question_answer = QuestionAnswer.query.filter(QuestionAnswer.id == question_answer_id).first()
        if existing_question_answer is None:
            raise DatabaseItemDoesNotExist('No QuestionAnswer with id {0}'.format(question_answer_id))
        return existing_question_answer

    def query(self, input_data):
        """
        Query for a QuestionAnswer where question_id, answer_id, user_id and user_report_id equal the input.
        Return QuestionAnswer or throw DatabaseItemDoesNotExist
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_question_answer = QuestionAnswer.query.filter(
            and_(QuestionAnswer.user_report_id == cleaned_data['user_report_id'],
                 QuestionAnswer.user_id == cleaned_data['user_id'],
                 QuestionAnswer.question_id == cleaned_data['question_id'],
                 QuestionAnswer.answer_id == cleaned_data['answer_id'])).first()
        if existing_question_answer is None:
            raise DatabaseItemDoesNotExist(
                'No QuestionAnswer with user_report_id {0}, user_id {1}, question_id {2} and answer_id {3}'.format(
                    cleaned_data['user_report_id'], cleaned_data['user_id'], cleaned_data['question_id'],
                    cleaned_data['answer_id']
                ))
        return existing_question_answer

    def update(self, question_answer_id, input_data):
        cleaned_data = self.parse_input_data(input_data)
        existing_question_answer = self.read(question_answer_id)
        existing_question_answer = self.update_simple_attributes(existing_question_answer, self.simple_params,
                                                                 cleaned_data)
        db.session.commit()
        return existing_question_answer

    def delete(self, question_answer_id):
        existing_question_answer = self.read(question_answer_id)
        db.session.delete(existing_question_answer)
        db.session.commit()
        return True

    def list(self):
        existing_question_answers = QuestionAnswer.query.all()
        return existing_question_answers

    def get_for_section_by_question_id(self, section_id, user_id, user_report_id):
        """
        Get all questionAnswers for a specific section (section_id) in a dict
        where the key is the question_id, for a specific user in a specific UserReport
        :param section_id:
        :param user_id:
        :param user_report_id:
        :return:
        """
        section_api = SectionApi()
        current_section = section_api.read(section_id)
        ordered_questions = {}
        for question in current_section.questions:
            if question.id in ordered_questions:
                raise DatabaseItemAlreadyExists('Error: two questions with the same id in one section!')
            # Get the QuestionAnswers object
            try:
                question_answer = self.get_answer_by_question_id(question.id, user_id, user_report_id)
            except DatabaseItemDoesNotExist:
                continue
            ordered_questions[question.id] = question_answer
        return ordered_questions

    def get_answer_by_question_id(self, question_id, user_id, user_report_id):
        """
        Get the answer to a question by its question_id in a specific report.
        :param question_id:
        :param user_id:
        :param user_report_id:
        :return:
        """
        question_answer = QuestionAnswer.query.filter(and_(QuestionAnswer.question_id == question_id,
                                                           QuestionAnswer.user_id == user_id,
                                                           QuestionAnswer.user_report_id == user_report_id)).first()
        if question_answer is None:
            raise DatabaseItemDoesNotExist('No answer found for question {0} in report {1}'.format(question_id,
                                                                                                   user_report_id))
        return question_answer

    def parse_input_data(self, input_data):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parameters have been filled. All missing parameters are set to None
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input_data(Section, input_data, self.possible_params, self.required_params,
                                             self.complex_params)
        return cleaned_data
