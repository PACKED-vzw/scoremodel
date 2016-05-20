from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, \
    IllegalEntityType
from scoremodel.modules.msg.messages import public_api_msg, public_error_msg


class QuestionAnswerQueryRestApi(ScoremodelRestApi):

    def get(self, item_id, input_data):
        try:
            found_object = self.api.query(input_data)
        except DatabaseItemDoesNotExist:
            self.msg =public_error_msg['item_not_exists'].format(self.api, item_id)
            self.status_code = 404
            found_object = None
        except Exception as e:
            self.msg =public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            found_object = None
        else:
            self.msg =public_api_msg['item_read'].format(self.api, item_id)
        if found_object is not None:
            return found_object.output_obj()
        else:
            return u''


class QuestionAnswerQuestionQueryRestApi(ScoremodelRestApi):
    def get(self, item_id, input_data):
        try:
            found_object = self.api.query_user_report_question(input_data)
        except DatabaseItemDoesNotExist:
            self.msg =public_error_msg['item_not_exists'].format(self.api, item_id)
            self.status_code = 404
            found_object = None
        except Exception as e:
            self.msg =public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            found_object = None
        else:
            self.msg =public_api_msg['item_read'].format(self.api, item_id)
        if found_object is not None:
            return found_object.output_obj()
        else:
            return u''

