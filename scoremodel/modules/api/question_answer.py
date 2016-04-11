from scoremodel.models.public import UserReport, QuestionAnswer
from scoremodel.models.general import Report, Section
from sqlalchemy import and_, or_
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel import db


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
