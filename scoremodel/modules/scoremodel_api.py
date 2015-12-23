import json
from scoremodel.modules.api import *
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, IllegalEntityType
from scoremodel import db


class ScoremodelApi:
    """
    Return the item in JSON
    """
    entity_types = {
        'question': QuestionApi,
        #'section': SectionApi,
        #'report': ReportApi,
        #'UserReport': UserReportApi,
        #'UserAnswer': UserAnswerApi
    }

    def __init__(self, request_body, entity_type):
        self.request_body = request_body
        if entity_type not in self.entity_types:
            raise IllegalEntityType('Entity type {0} does not exist!'.format(entity_type))
        self.entity = self.entity_types[entity_type]()

    def create(self):
        """
        The request body is in JSON
        :param request_body:
        :param entity_type:
        :return:
        """
        input_data = json.loads(self.request_body)  # ValueError
