from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemDoesNotExist
from scoremodel.models.general import Section, Answer, Action, Report, RiskFactor, Question
from sqlalchemy import and_, or_


class GenericApi:

    def clean_input_data(self, input_data, possible_params, required_params, complex_params):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parametes have been filled. All missing parameters are set to None. All attributes in complex_params
        must be a list.
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
                raise RequiredAttributeMissing('Missing {0} in input_data'.format(required_param))
        # Set the missing attributes from possible_params in input_data to None
        for possible_param in possible_params:
            if possible_param not in cleaned:
                cleaned[possible_param] = None
        # Check whether the complex parameters are lists
        for complex_param in complex_params:
            if type(cleaned[complex_param]) is not list:
                cleaned[complex_param] = [cleaned[complex_param]]
        return cleaned

    def get_answer(self, answer_name):
        answer = Answer.query.filter(Answer.answer == answer_name).first()
        if answer is None:
            raise DatabaseItemDoesNotExist('No answer called {0}'.format(answer_name))
        return answer

    def get_action(self, action_name):
        action = Action.query.filter(Action.action == action_name).first()
        if action is None:
            raise DatabaseItemDoesNotExist('No action called {0}'.format(action_name))
        return action

    def get_risk_factor(self, risk_factor_name):
        risk_factor = RiskFactor.query.filter(RiskFactor.risk_factor == risk_factor_name).first()
        if risk_factor is None:
            raise DatabaseItemDoesNotExist('No risk factor called {0}'.format(risk_factor_name))
        return risk_factor

    def get_question(self, question_name, section_id):
        existing_question = Question.query.filter(and_(Question.question == question_name,
                                                         Question.section_id == section_id)).first()
        if existing_question is None:
            raise DatabaseItemDoesNotExist('No question called {0} in section {1}'.format(question_name, section_id))
        return existing_question

    def get_section(self, section_title, report_id):
        existing_section = Section.query.filter(and_(Section.title == section_title,
                                                       Section.report_id == report_id)).first()
        if existing_section is None:
            raise DatabaseItemDoesNotExist('No section called {0} in report {1}'.format(section_title, report_id))
        return existing_section

    def update_entity_attribute(self, entity, attribute_name, attribute_new_value):
        """
        This function updates the attribute attribute_name of entity only if the original value
        is different from attribute_new_value
        :param entity:
        :param attribute_name:
        :param attribute_value:
        :return:
        """
        original_value = getattr(entity, attribute_name)
        if original_value != attribute_new_value:
            setattr(entity, attribute_name, attribute_new_value)
        return entity

    def update_simple_attributes(self, entity, simple_attributes, cleaned_data):
        """
        Use self.update_entity_attribute() to update the simple (string or numeric) attributes of entity with
        cleaned_data.
        :param entity:
        :param simple_attributes:
        :param cleaned_data:
        :return:
        """
        for simple_attribute in simple_attributes:
            entity = self.update_entity_attribute(entity, simple_attribute, cleaned_data[simple_attribute])
        return entity
