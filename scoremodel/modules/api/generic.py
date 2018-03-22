from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemDoesNotExist
from scoremodel.models.general import Section, Answer, Report, RiskFactor, Question
from sqlalchemy import and_, or_
from datetime import datetime
from pytz import timezone
import abc


class GenericApi:

    __metaclass__ = abc.ABCMeta

    # Abstract methods

    @abc.abstractmethod
    def create(self, object_data):
        return

    @abc.abstractmethod
    def read(self, object_id):
        return

    @abc.abstractmethod
    def update(self, object_id, object_data):
        return

    @abc.abstractmethod
    def delete(self, object_id):
        return

    @abc.abstractmethod
    def list(self):
        return

    # Helper methods

    def clean_input_data(self, db_class, input_data, possible_params, required_params, complex_params):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parameters have been filled. All missing parameters are set to None. All attributes in complex_params
        must be a list.
        :param db_class
        :param input_data:
        :param required_params
        :param possible_params
        :param complex_params
        :return:
        """
        cleaned = {}
        # All non-supported parameters are filtered
        for input_data_key, input_data_value in input_data.items():
            if input_data_key in possible_params:
                cleaned[input_data_key] = input_data_value
        # Check whether the required parameters are used
        for required_param in required_params:
            if required_param not in input_data:
                raise RequiredAttributeMissing(_e['attr_missing'].format(required_param))
        # Set the missing attributes from possible_params in input_data to None
        for possible_param in possible_params:
            if possible_param not in cleaned:
                cleaned[possible_param] = None
        # Check whether the complex parameters are lists
        for complex_param in complex_params:
            if type(cleaned[complex_param]) is not list:
                if cleaned[complex_param] is not None:
                    cleaned[complex_param] = [cleaned[complex_param]]
                else:
                    cleaned[complex_param] = []
        # Check for nullability
        for possible_param in possible_params:
            if possible_param in db_class.__table__.columns:
                if db_class.__table__.columns[possible_param].nullable is not True:
                    # Can't be null, so set it to 0 or empty string or empty date, depending on what the type is
                    if cleaned[possible_param] is None:
                        c_type = str(db_class.__table__.columns[possible_param].type)
                        ##
                        # TODO make this cleaner
                        ##
                        if c_type == 'INTEGER':
                            cleaned[possible_param] = 0
                        elif c_type == 'TEXT':
                            cleaned[possible_param] = u''
                        elif c_type == 'DATETIME':
                            cleaned[possible_param] = datetime.now(tz=timezone('UTC'))
                        elif c_type == 'STRING':
                            cleaned[possible_param] = u''
        return cleaned

    def get_answer(self, answer_name):
        answer = Answer.query.filter(Answer.answer == answer_name).first()
        if answer is None:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Answer, answer_name))
        return answer

    def get_risk_factor(self, risk_factor_name):
        risk_factor = RiskFactor.query.filter(RiskFactor.risk_factor == risk_factor_name).first()
        if risk_factor is None:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(RiskFactor, risk_factor_name))
        return risk_factor

    def get_question(self, question_name, section_id):
        existing_question = Question.query.filter(and_(Question.question == question_name,
                                                         Question.section_id == section_id)).first()
        if existing_question is None:
            raise DatabaseItemDoesNotExist(_e['item_not_in'].format(Question, question_name, Section, section_id))
        return existing_question

    def get_section(self, section_title, report_id):
        existing_section = Section.query.filter(and_(Section.title == section_title,
                                                     Section.report_id == report_id)).first()
        if existing_section is None:
            raise DatabaseItemDoesNotExist(_e['item_not_in'].format(Section, section_title, Report, report_id))
        return existing_section

    def update_entity_attribute(self, entity, attribute_name, attribute_new_value):
        """
        This function updates the attribute attribute_name of entity only if the original value
        is different from attribute_new_value.
        :param entity:
        :param attribute_name:
        :param attribute_value:
        :return:
        """
        original_value = getattr(entity, attribute_name)
        if original_value != attribute_new_value:
            setattr(entity, attribute_name, attribute_new_value)
        return entity

    def update_simple_attributes(self, entity, simple_attributes, cleaned_data, to_skip=()):
        """
        Use self.update_entity_attribute() to update the simple (string or numeric) attributes of entity with
        cleaned_data. Attributes in to_skip are skipped.
        :param entity:
        :param simple_attributes:
        :param cleaned_data:
        :param to_skip:
        :return:
        """
        for simple_attribute in simple_attributes:
            if simple_attribute not in to_skip:
                entity = self.update_entity_attribute(entity, simple_attribute, cleaned_data[simple_attribute])
        return entity
