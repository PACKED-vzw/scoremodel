from scoremodel.models.general import Action
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class ActionApi(GenericApi):
    complex_params = []  # These should be a list in input_data
    simple_params = ['action']

    def __init__(self, action_id=None):
        self.action_id = action_id

    def create(self, input_data):
        """
        Create a new action and return the action object. See QuestionApi for a more in-depth explanation of
        how this function works. Fails when the action already exists.
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        # Check whether an action like this exists
        try:
            existing_action = self.get_action(cleaned_data['action'])
        except DatabaseItemDoesNotExist:
            existing_action = None
        if existing_action:
            raise DatabaseItemAlreadyExists('An action called "{0}" already exists.'.format(cleaned_data['action']))
        new_action = Action(action=cleaned_data['action'])
        db.session.add(new_action)
        db.session.commit()
        return new_action

    def read(self, action_id):
        """
        Return an action by its id
        :param action_id:
        :return:
        """
        existing_action = Action.query.filter(Action.id == action_id).first()
        if existing_action is None:
            raise DatabaseItemDoesNotExist('No action with id {0)'.format(action_id))
        return existing_action

    def update(self, action_id, input_data):
        """
        Update an action with input_data. See self.create() and QuestionApi.update().
        :param action_id:
        :param input_data:
        :return:
        """
        existing_action = self.read(action_id)
        cleaned_data = self.parse_input_data(input_data)
        existing_action = self.update_simple_attributes(existing_action, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_action

    def delete(self, action_id):
        """
        Delete an action. See QuestionApi.delete()
        :param action_id:
        :return:
        """
        existing_action = self.read(action_id)
        db.session.delete(existing_action)
        db.session.commit()
        return True

    def parse_input_data(self, input_data):
        possible_params = ['action']
        required_params = ['action']
        return self.clean_input_data(Action, input_data, possible_params, required_params, self.complex_params)
