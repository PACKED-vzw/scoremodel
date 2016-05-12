from scoremodel.models.general import Question, Answer, RiskFactor, Report, Section
from sqlalchemy import and_, or_
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.answer import AnswerApi
import scoremodel.modules.api.section
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel import db


class QuestionApi(GenericApi):
    simple_attributes = ['question', 'context', 'risk', 'example', 'weight', 'order_in_section', 'section_id', 'action', 'risk_factor_id']
    complex_params = ['answers']  # These should be a list in input_data

    def __init__(self, question_id=None):
        self.question_id = question_id
        self.a_section = scoremodel.modules.api.section.SectionApi()
        self.a_risk_factor = RiskFactorApi()

    def create(self, input_data):
        """
        Create a new question. The data input variable contains all the attributes for the "question" entity
        in the database as a dict. For simple attributes, this is a string or integer value, but for actions,
        answers and risk factors, it is a dictionary containing the attributes for the respective entity
        in the database.
        The function will fail when a question with the same "question" attribute already exists in the same
        section. Submitting actions, answers or risk factors that already exist will not result in an error.
        The function returns the question sqlalchemy object.
        :param data:
        :param section_id:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        # Check whether this question already exists
        existing_question = Question.query.filter(and_(Question.question == cleaned_data['question'],
                                                       Question.section_id == cleaned_data['section_id'])).first()
        if existing_question:
            # Already exists
            raise DatabaseItemAlreadyExists('A question called "{0}" already exists in this section.'
                                            .format(cleaned_data['question']))
        new_question = Question(question=cleaned_data['question'], context=cleaned_data['context'],
                                risk=cleaned_data['risk'], example=cleaned_data['example'],
                                weight=cleaned_data['weight'], order=cleaned_data['order_in_section'],
                                action=cleaned_data['action'])
        db.session.add(new_question)
        db.session.commit()
        # Add to the section
        section = self.a_section.read(cleaned_data['section_id'])
        new_question.section = section
        # Add the answers
        for answer in cleaned_data['answers']:
            new_question.answers.append(self.new_answer(answer))
        # Add the risk factor
        risk_factor = self.a_risk_factor.read(cleaned_data['risk_factor_id'])
        new_question.risk_factor = risk_factor
        # Store everything in the database
        db.session.commit()
        # Return the question object
        return new_question

    def read(self, question_id):
        """
        Get a question from the database by its ID
        :param question_id:
        :return:
        """
        existing_question = Question.query.filter(Question.id == question_id).first()
        if existing_question is None:
            raise DatabaseItemDoesNotExist('No question with id {0}'.format(question_id))
        return existing_question

    def update(self, question_id, input_data):
        """
        Update a question identified by question_id. The variable input_data must contain all variables, both
        those that are to be changed and those that remain the same. If you only send the changed ones, the others
        will be set to None. It follows the same logic as self.create(), but it doesn't die when the question already
        exists (but it does when it doesn't).
        :param question_id:
        :param input_data:
        :param section_id:
        :return:
        """
        existing_question = self.read(question_id)
        cleaned_data = self.parse_input_data(input_data)
        existing_question = self.update_simple_attributes(existing_question, self.simple_attributes, cleaned_data)
        # Update the section
        section = self.a_section.read(cleaned_data['section_id'])
        existing_question.section = section
        # Update answers
        existing_question = self.remove_answers(existing_question)
        for answer in cleaned_data['answers']:
            existing_question.answers.append(self.new_answer(answer))
        # Update risk factors
        risk_factor = self.a_risk_factor.read(cleaned_data['risk_factor_id'])
        existing_question.risk_factor = risk_factor
        db.session.commit()
        return existing_question

    def delete(self, question_id):
        """
        Delete a question by its ID. Fails when it doesn't exist.
        :param question_id:
        :return:
        """
        existing_question = self.read(question_id)
        db.session.delete(existing_question)
        db.session.commit()
        return True

    def parse_input_data(self, input_data):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parameters have been filled. All missing parameters are set to None
        :param input_data:
        :return:
        """
        # Solve legacy applications that use risk_factors (a list) instead of risk_factor (an object). Multiple
        # risk factors for one question are no longer supported.
        if 'risk_factors' in input_data:
            raise RequiredAttributeMissing('Error: risk_factors was provided!')
        possible_params = ['question', 'context', 'risk', 'example', 'weight', 'order_in_section', 'action',
                           'risk_factor_id', 'answers', 'section_id']
        required_params = ['question', 'weight', 'section_id']
        return self.clean_input_data(Question, input_data, possible_params, required_params, self.complex_params)

    def new_answer(self, answer_data):
        # Check whether this answer exists
        a_answer = AnswerApi()
        cleaned_data = a_answer.parse_input_data(answer_data)
        try:
            o_answer = self.get_answer(cleaned_data['answer'])
        except DatabaseItemDoesNotExist:
            # Create it if it doesn't
            o_answer = a_answer.create(cleaned_data)
        return o_answer

    def remove_answers(self, question_entity):
        for answer in question_entity.answers:
            question_entity.answers.remove(answer)
        db.session.commit()
        return question_entity

