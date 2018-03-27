from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Question, Answer
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.lang import LangApi
from scoremodel import db


class AnswerApi(GenericApi):
    complex_params = []  # These should be a list in input_data
    simple_params = ['answer', 'value', 'lang_id']
    possible_params = ['answer', 'value', 'lang_id']
    required_params = ['answer', 'lang_id']

    def __init__(self, answer_id=None):
        self.answer_id = answer_id
        self.lang_api = LangApi()

    def create(self, input_data):
        """
        Create a new answer from input_data. See QuestionApi.create()
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        try:
            existing_answer = self.get_answer(cleaned_data['answer'])
        except DatabaseItemDoesNotExist:
            existing_answer = None
        if existing_answer:
            raise DatabaseItemAlreadyExists(_e['item_exists'].format(Answer, cleaned_data['answer']))
        new_answer = Answer(answer=cleaned_data['answer'], value=cleaned_data['value'], lang_id=cleaned_data['lang_id'])
        db.session.add(new_answer)
        db.session.commit()
        return new_answer

    def read(self, answer_id):
        """
        Return an answer by its id. See QuestionApi.read()
        :param answer_id:
        :return:
        """
        existing_answer = Answer.query.filter(Answer.id == answer_id).first()
        if existing_answer is None:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Answer, answer_id))
        return existing_answer

    def update(self, answer_id, input_data):
        """
        Update an existing answer. See QuestionApi.update()
        :param answer_id:
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_answer = self.read(answer_id)
        existing_answer = self.update_simple_attributes(existing_answer, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_answer

    def delete(self, answer_id):
        """
        Delete an existing answer. See QuestionApi.delete()
        :param answer_id:
        :return:
        """
        existing_answer = self.read(answer_id)
        db.session.delete(existing_answer)
        db.session.commit()
        return True

    def list(self):
        """
        List all answers
        :return:
        """
        answers = Answer.query.all()
        return answers

    def by_lang(self, lang):
        """
        List all answers in a given language
        :return:
        """
        existing_lang = self.lang_api.by_lang(lang)
        existing_answers = Answer.query.filter(Answer.lang_id == existing_lang.id).all()
        return existing_answers

    def parse_input_data(self, input_data):
        cleaned_data = self.clean_input_data(Answer, input_data, self.possible_params, self.required_params,
                                             self.complex_params)
        # When updating, optional values that are not present are not automatically assigned their default values
        if 'value' not in cleaned_data or cleaned_data['value'] is None:
            cleaned_data['value'] = 1
        return cleaned_data
