from flask.ext.babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Report
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.lang import LangApi
from scoremodel import db


class ReportApi(GenericApi):
    simple_params = ['title', 'lang_id']
    complex_params = []

    def __init__(self, report_id=None):
        self.report_id = report_id
        self.lang_api = LangApi()
        self.created = []

    def create(self, input_data):
        """
        Create a new report. See QuestionApi.create()
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_report = Report.query.filter(Report.title == cleaned_data['title']).first()
        if existing_report is not None:
            raise DatabaseItemAlreadyExists(_e['item_exists'].format(Report, cleaned_data['title']))
        new_report = Report(title=cleaned_data['title'], lang_id=cleaned_data['lang_id'])
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
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Report, report_id))
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

    def list(self):
        """
        List all reports
        :return:
        """
        existing_reports = Report.query.all()
        return existing_reports

    def by_lang(self, lang):
        """
        List all reports in a given language
        :return:
        """
        existing_lang = self.lang_api.by_lang(lang)
        existing_reports = Report.query.filter(Report.lang_id == existing_lang.id).all()
        return existing_reports

    def parse_input_data(self, input_data):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parametes have been filled. All missing parameters are set to None
        :param input_data:
        :return:
        """
        possible_params = ['title', 'lang_id']
        required_params = ['title', 'lang_id']
        return self.clean_input_data(Report, input_data, possible_params, required_params, self.complex_params)
