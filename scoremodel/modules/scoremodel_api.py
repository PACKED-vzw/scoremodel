import json
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist, IllegalEntityType


class ScoremodelApi:
    def __init__(self, api_class):
        self.api = api_class()

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
