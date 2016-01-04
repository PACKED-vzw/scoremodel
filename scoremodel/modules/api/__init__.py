import json
from flask import make_response
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, \
    IllegalEntityType
from scoremodel.modules.msg.messages import api_msg, error_msg


class ScoremodelApi:
    def __init__(self, api_class, o_request, api_obj_id=None):
        self.api = api_class()
        self.request = o_request
        self.msg = None
        self.output_data = u''
        ##
        # Every request method has a self.action() defined:
        #   GET => self.read(api_obj_id)
        #   DELETE => self.delete(api_obj_id)
        #   PUT => self.update(api_obj_id)
        #   POST => self.create()
        ##
        input_data_raw = self.request.get_data()
        input_data_string = input_data_raw.decode('utf-8')
        if self.request.method == 'GET':
            if api_obj_id is None:
                self.msg = error_msg['missing_argument'].format('api_obj_id')
            else:
                self.output_data = self.read(api_obj_id)
        elif self.request.method == 'DELETE':
            if api_obj_id is None:
                self.msg = error_msg['missing_argument'].format('api_obj_id')
            else:
                self.output_data = self.delete(api_obj_id)
        elif self.request.method == 'PUT':
            if api_obj_id is None:
                self.msg = error_msg['missing_argument'].format('api_obj_id')
            else:
                if self.parse_json(input_data_string) is not None:
                    self.output_data = self.update(api_obj_id, self.parse_json(input_data_string))
        elif self.request.method == 'POST':
            if self.parse_json(input_data_string) is not None:
                self.output_data = self.parse_json(input_data_string)
        else:
            self.msg = error_msg['illegal_action'].format(self.request.method)
        ##
        # Set self.response
        ##
        self.response = self.create_response(self.output_data)

    def create(self, input_data, additional_opts=None):
        if not additional_opts:
            additional_opts = {}
        try:
            created_object = self.api.create(input_data=input_data, **additional_opts)
        except DatabaseItemAlreadyExists:
            self.msg = error_msg['item_exists'].format(self.api)
            created_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            created_object = None
        else:
            self.msg = api_msg['item_created'].format(self.api, created_object.id)
        if created_object is not None:
            return created_object.output_obj()
        else:
            return u''

    def read(self, item_id):
        try:
            found_object = self.api.read(item_id)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            found_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            found_object = None
        else:
            self.msg = api_msg['item_read'].format(self.api, item_id)
        if found_object is not None:
            return found_object.output_obj()
        else:
            return u''

    def update(self, item_id, input_data, additional_opts=None):
        if not additional_opts:
            additional_opts = {}
        try:
            updated_object = self.api.update(item_id, input_data=input_data, **additional_opts)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            updated_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            updated_object = None
        else:
            self.msg = api_msg['item_updated'].format(self.api, updated_object.id)
        if updated_object is not None:
            return updated_object.output_obj()
        else:
            return u''

    def delete(self, item_id):
        try:
            deleted_object = self.api.delete(item_id)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            deleted_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            deleted_object = None
        else:
            self.msg = api_msg['item_deleted'].format(self.api, item_id)
        if deleted_object is True:
            return u''
        else:
            return u''

    def create_response(self, data):
        """
        Create an API response
        :param data:
        :param msg:
        :return:
        """
        resp = make_response()
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.data = json.dumps({
            'msg': self.msg,
            'data': data
        })
        return resp

    def parse_json(self, unparsed_string):
        try:
            parsed_string = json.loads(unparsed_string)
        except ValueError as e:
            self.msg = u'A JSON error occurred: {0}'.format(e)
            return None
        return parsed_string
