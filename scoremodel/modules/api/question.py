from flask.ext.babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Question, Answer, RiskFactor, Report, Section
from sqlalchemy import and_, or_
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.answer import AnswerApi
import scoremodel.modules.api.section
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel import db


class QuestionApi(GenericApi):
    simple_attributes = ['question', 'context', 'risk', 'example', 'weight', 'order_in_section', 'section_id', 'action',
                         'risk_factor_id']
    complex_params = ['answers']  # These should be a list in input_data

    def __init__(self, question_id=None, autocommit=True):
        self.question_id = question_id
        self.a_section = scoremodel.modules.api.section.SectionApi()
        self.a_risk_factor = RiskFactorApi()
        self.autocommit = autocommit

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
        if self.db_exists(cleaned_data['question'], cleaned_data['section_id']):
            raise DatabaseItemAlreadyExists(_e['item_already_in'].format(Question, cleaned_data['question'], Section,
                                                                         cleaned_data['section_id']))
        return self.db_create(cleaned_data, self.a_section.read(cleaned_data['section_id']),
                              self.db_get_answers(cleaned_data['answers']),
                              self.a_risk_factor.read(cleaned_data['risk_factor_id']))

    def read(self, question_id):
        """
        Get a question from the database by its ID
        :param question_id:
        :return:
        """
        existing_question = Question.query.filter(Question.id == question_id).first()
        if existing_question is None:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Question, question_id))
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
        return self.db_update(existing_question, cleaned_data, self.a_section.read(cleaned_data['section_id']),
                              self.db_get_answers(cleaned_data['answers']),
                              self.a_risk_factor.read(cleaned_data['risk_factor_id']))

    def delete(self, question_id):
        """
        Delete a question by its ID. Fails when it doesn't exist.
        :param question_id:
        :return:
        """
        existing_question = self.read(question_id)
        db.session.delete(existing_question)
        self.store()
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
            raise RequiredAttributeMissing(_('Error: risk_factors was provided!'))
        possible_params = ['question', 'context', 'risk', 'example', 'weight', 'order_in_section', 'action',
                           'risk_factor_id', 'answers', 'section_id']
        required_params = ['question', 'weight', 'section_id']
        return self.clean_input_data(Question, input_data, possible_params, required_params, self.complex_params)

    def get_answer(self, answer_id):
        # Check whether this answer exists
        a_answer = AnswerApi()
        o_answer = a_answer.read(answer_id)
        return o_answer

    def remove_answers(self, question_entity):
        for answer in question_entity.answers:
            question_entity.answers.remove(answer)
        self.store()
        return question_entity

    def query(self, question_question):
        """
        Select a question by its name ("question"): this attribute is unique
        :param question_question:
        :return:
        """
        existing_question = Question.query.filter(Question.question == question_question).first()
        if not existing_question:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Question, question_question))
        return existing_question

    def store(self):
        if self.autocommit:
            db.session.commit()

    def db_get_answers(self, answer_ids):
        """
        From a list of answer ids, get the list of answer database objects
        :param answer_ids:
        :return:
        """
        answers = []
        for answer_id in answer_ids:
            answers.append(self.get_answer(answer_id))
        return answers

    def db_update(self, existing_question, cleaned_data, section, answers, risk_factor):
        """
        See self.db_create() why this function exists.
        :param existing_question:
        :param cleaned_data:
        :param section:
        :param answers:
        :param risk_factor:
        :return:
        """
        existing_question = self.update_simple_attributes(existing_question, self.simple_attributes, cleaned_data)
        # Update the section
        existing_question.section = section
        # Update answers
        existing_question = self.remove_answers(existing_question)
        for answer in answers:
            existing_question.answers.append(answer)
        # Update risk factors
        existing_question.risk_factor = risk_factor
        self.store()
        return existing_question

    def db_create(self, cleaned_data, section, answers, risk_factor):
        """
        Create a question. This is a collection of all the write actions to the database, so we can wrap
        them in a transaction. We have to separate the "read" (query) actions as SQLAlchemy commits everything
        before querying (http://docs.sqlalchemy.org/en/latest/orm/session_basics.html).
        :param cleaned_data:
        :param section:
        :param answers:
        :param risk_factor:
        :return:
        """
        new_question = Question(question=cleaned_data['question'], context=cleaned_data['context'],
                                risk=cleaned_data['risk'], example=cleaned_data['example'],
                                weight=cleaned_data['weight'], order=cleaned_data['order_in_section'],
                                action=cleaned_data['action'])
        db.session.add(new_question)
        # Add to the section
        new_question.section = section
        # Add the answers
        for answer in answers:
            new_question.answers.append(answer)
        # Add the risk factor
        new_question.risk_factor = risk_factor
        # Store everything in the database
        self.store()
        # Return the question object
        return new_question

    def db_exists(self, question_question, section_id):
        """

        :param question_question:
        :param section_id:
        :return:
        """
        existing_question = Question.query.filter(and_(Question.question == question_question,
                                                       Question.section_id == section_id)).first()
        if existing_question:
            return True
        return False
