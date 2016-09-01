import json
from werkzeug.exceptions import BadRequest
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, \
    IllegalEntityType
from scoremodel.modules.msg.messages import public_api_msg, public_error_msg
from scoremodel.modules.api.rest import RestApi


class ScoremodelRestApi:

    ##
    # This table translates between API methods
    # and api_class methods. Useful when you want
    # to use another function to perform a .read().
    translation_table = {
        'post': 'create',
        'get': 'read',
        'put': 'update',
        'delete': 'delete',
        'list': 'list'
    }

    def __init__(self, api_class, o_request, api_obj_id=None, hooks=(), translate=None, additional_opts=None):
        """
        This class is an REST API class that translates between request methods and
        methods of the api_class class.
        It performs the following functions:
            - Translate between request.method and self.action()
                GET => self.get(api_obj_id) | self.list() if api_obj_id is None
                DELETE => self.delete(api_obj_id)
                POST => self.post(o_request.get_data().decode())
                PUT => self.put(api_obj_id, o_request.get_data().decode())
            - Translate between self.action() and api_class.action() using translate or self.translation_table
                if translate is None.
            - Performs functions in hooks on the decoded but unparsed data from the original request.
                All functions take input_data_string as input and must return it (after they applied their actions).
                The order of the hooks can not be guaranteed.
            - Converts the request data to JSON.
            - Takes the reply from api_class (in JSON) and convert it to a response with the correct
                status code and headers.
            - On error: generate an error message, error code and error status code.
        :param api_class:
        :param o_request:
        :param api_obj_id:
        :param hooks:
        :param translate:
        :param additional_opts:
        """
        self.api = api_class()
        self.request = o_request
        self.msg = None
        self.output_data = u''
        self.status_code = 200
        # TODO: check for completeness
        if translate is None:
            self.translate = self.translated_functions(self.translation_table)
        else:
            self.translate = self.translated_functions(translate)
        ##
        # Normally we would use .get_data() and convert the bytes to a string
        # but CsrfProtect() already parses the form, thus emptying .get_data()
        # We use this trick so all other functions remain unchanged.
        # Note that we still have to implement some kind of error reporting when
        # the automatic parsing fails.
        ##
        input_data_json = {}
        if self.request.method != 'GET' and self.request.method != 'DELETE':
            try:
                input_data_json = self.request.get_json(force=True, silent=False)
            except BadRequest as e:
                self.msg = public_error_msg['error_occurred'].format(e)
                self.status_code = 400
        if self.status_code != 400:
            try:
                for hook in hooks:
                    input_data_json = hook(input_data_json)
            except Exception as e:
                self.msg = public_error_msg['error_occurred'].format(e)
                self.status_code = 400
            else:
                self.parse_request(input_data_json=input_data_json, api_obj_id=api_obj_id,
                                   additional_opts=additional_opts)
        ##
        # Set self.response
        ##
        self.response = self.create_response(self.output_data)

    def post(self, input_data, additional_opts=None):
        if not additional_opts:
            additional_opts = {}
        try:
            created_object = self.translate['post'](input_data=input_data, **additional_opts)
        except DatabaseItemAlreadyExists:
            self.msg = public_error_msg['item_exists'].format(self.api)
            self.status_code = 400
            created_object = None
        except DatabaseItemDoesNotExist:
            self.msg = public_error_msg['item_not_exists'].format(self.api)
            self.status_code = 404
            created_object = None
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            created_object = None
        else:
            self.msg = public_api_msg['item_created'].format(self.api, created_object.id)
        if created_object is not None:
            return created_object.output_obj()
        else:
            return u''

    def get(self, item_id, input_data, additional_opts=None):
        try:
            found_object = self.translate['get'](item_id)
        except DatabaseItemDoesNotExist:
            self.msg = public_error_msg['item_not_exists'].format(self.api, item_id)
            self.status_code = 404
            found_object = None
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            found_object = None
        else:
            self.msg = public_api_msg['item_read'].format(self.api, item_id)
        if found_object is not None:
            return found_object.output_obj()
        else:
            return u''

    def list(self, additional_opts=None):
        try:
            found_objects = self.api.list()
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            found_objects = None
        if found_objects is not None:
            self.msg = public_api_msg['items_found'].format(self.api)
            out_results = []
            for found_object in found_objects:
                out_results.append(found_object.output_obj())
            return out_results
        else:
            return u''

    def put(self, item_id, input_data, additional_opts=None):
        if not additional_opts:
            additional_opts = {}
        try:
            updated_object = self.api.update(item_id, input_data=input_data, **additional_opts)
        except DatabaseItemDoesNotExist:
            self.msg = public_error_msg['item_not_exists'].format(self.api, item_id)
            self.status_code = 404
            updated_object = None
        except DatabaseItemAlreadyExists:
            self.msg = public_error_msg['item_exists'].format(self.api)
            self.status_code = 400
            updated_object = None
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            updated_object = None
        else:
            self.msg = public_api_msg['item_updated'].format(self.api, updated_object.id)
        if updated_object is not None:
            return updated_object.output_obj()
        else:
            return u''

    def delete(self, item_id, additional_opts=None):
        try:
            deleted_object = self.api.delete(item_id)
        except DatabaseItemDoesNotExist:
            self.msg = public_error_msg['item_not_exists'].format(self.api, item_id)
            self.status_code = 404
            deleted_object = False
        except Exception as e:
            self.msg = public_error_msg['error_occurred'].format(e)
            self.status_code = 400
            deleted_object = False
        else:
            self.msg = public_api_msg['item_deleted'].format(self.api, item_id)
        if deleted_object is True:
            return u''
        else:
            return u''

    def parse_get(self, api_obj_id=None, input_data_json=None, additional_opts=None):
        """
        Parse a GET request
        :param api_obj_id:
        :param input_data_json:
        :param additional_opts:
        :return:
        """
        if api_obj_id is None:
            if hasattr(self.api, 'list'):
                self.output_data = self.list(additional_opts=additional_opts)
            else:
                self.msg = public_error_msg['missing_argument'].format('api_obj_id')
                self.status_code = 400
        else:
            self.output_data = self.get(api_obj_id, input_data_json)

    def parse_delete(self, api_obj_id=None, additional_opts=None):
        """
        Parse a DELETE request
        :param api_obj_id:
        :param additional_opts:
        :return:
        """
        if api_obj_id is None:
            self.msg = public_error_msg['missing_argument'].format('api_obj_id')
            self.status_code = 400
        else:
            self.output_data = self.delete(api_obj_id, additional_opts=additional_opts)

    def parse_put(self, api_obj_id=None, input_data_json=None, additional_opts=None):
        """
        Parse a PUT request
        :param api_obj_id:
        :param input_data_json:
        :param additional_opts:
        :return:
        """
        if api_obj_id is None:
            self.msg = public_error_msg['missing_argument'].format('api_obj_id')
            self.status_code = 400
        else:
            if input_data_json is not None:
                self.output_data = self.put(api_obj_id, input_data_json,
                                            additional_opts=additional_opts)
            else:
                self.msg = public_error_msg['missing_argument'].format('body')
                self.status_code = 400

    def parse_post(self, input_data_json, additional_opts=None):
        """
        Parse a POST request
        :param input_data_json:
        :param additional_opts:
        :return:
        """
        if input_data_json is not None:
            self.output_data = self.post(input_data_json, additional_opts=additional_opts)
        else:
            self.msg = public_error_msg['missing_argument'].format('body')
            self.status_code = 400

    def parse_request(self, input_data_json=None, api_obj_id=None, additional_opts=None):
        """
        Parse the original request:
            - Check for missing arguments and input
            - Execute self.action() for the request.method (self.request)
        This function has many sub functions (parse_*) to allow for easier
        subclassing.
        :param input_data_json: (parsed JSON request data)
        :param api_obj_id:
        :param additional_opts:
        :return:
        """
        if self.request.method == 'GET':
            self.parse_get(api_obj_id, input_data_json, additional_opts=additional_opts)
        elif self.request.method == 'DELETE':
            self.parse_delete(api_obj_id, additional_opts=additional_opts)
        elif self.request.method == 'PUT':
            self.parse_put(api_obj_id, input_data_json, additional_opts=additional_opts)
        elif self.request.method == 'POST':
            self.parse_post(input_data_json, additional_opts=additional_opts)
        else:
            self.msg = public_error_msg['illegal_action'].format(self.request.method)
            self.status_code = 405

    def create_response(self, data):
        """
        Create an API response
        :param data:
        :return:
        """
        rest_api = RestApi()
        return rest_api.response(status=self.status_code, data=data, msg=self.msg)

    def parse_json(self, unparsed_string):
        try:
            parsed_string = json.loads(unparsed_string)
        except ValueError as e:
            self.msg = u'A JSON error occurred: {0}'.format(e)
            return None
        return parsed_string

    def translated_functions(self, translation_table):
        """
        Take translation_table and self.api: return the function with that name in such a way
        that it can be called (https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-from-a-string-with-the-functions-name-in-python)
        :return:
        """
        translation = {}
        for our_function, api_function in translation_table.items():
            call_function = getattr(self.api, api_function)
            translation[our_function] = call_function
        return translation

    def csrf(self):
        """

        :return:
        """
        # Check the origin and referer headers
