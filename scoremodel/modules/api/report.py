from scoremodel.models.general import Report, Section
from sqlalchemy import and_, or_
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.section import SectionApi
from scoremodel import db


class ReportApi(GenericApi):
    simple_params = ['title']
    complex_params = []

    def __init__(self, report_id=None):
        self.report_id = report_id

    def create(self, input_data):
        """
        Create a new report. See QuestionApi.create()
        :param input_data: 
        :return: 
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_report = Report.query.filter(Report.title == cleaned_data['title']).first()
        if existing_report is not None:
            raise DatabaseItemAlreadyExists('A report called {0} already exists'.format(cleaned_data['title']))
        new_report = Report(title=cleaned_data['title'])
        db.session.add(new_report)
        db.session.commit()
        return new_report

    def read(self, report_id):
        """
        Get a report by its id. See QuestionApi.read()
        :param report_id: 
        :return: 
        """
        existing_report = Report.query.filter(Report.id == report_id).first()
        if existing_report is None:
            raise DatabaseItemDoesNotExist('No report with id {0}'.format(report_id))
        return existing_report

    def update(self, report_id, input_data):
        """
        Update an existing report. See QuestionApi.update()
        :param report_id:
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_report = self.read(report_id)
        existing_report = self.update_simple_attributes(existing_report, simple_attributes=self.simple_params,
                                                        cleaned_data=cleaned_data)
        db.session.commit()
        return existing_report

    def delete(self, report_id):
        """
        Delete an existing report. See QuestionApi.delete()
        :param report_id:
        :return:
        """
        existing_report = self.read(report_id)
        db.session.delete(existing_report)
        db.session.commit()
        return True

    def parse_input_data(self, input_data):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parametes have been filled. All missing parameters are set to None
        :param input_data:
        :return:
        """
        possible_params = ['title']
        required_params = ['title']
        return self.clean_input_data(input_data, possible_params, required_params, self.complex_params)
