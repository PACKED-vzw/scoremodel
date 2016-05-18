from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, \
    IllegalEntityType
from scoremodel.modules.msg.messages import api_msg, error_msg


class QuestionAnswerRestApi(ScoremodelRestApi):

    def get(self, item_id, input_data):
        try:
            found_object = self.api.query(input_data)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            self.status_code = 404
            found_object = None
        #except Exception as e:
        #    self.msg = error_msg['error_occurred'].format(e)
        #    self.status_code = 400
        #    found_object = None
        else:
            self.msg = api_msg['item_read'].format(self.api, item_id)
        if found_object is not None:
            return found_object.output_obj()
        else:
            return u''
