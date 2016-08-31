from flask.ext.babel import gettext as _
from sqlalchemy import and_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.benchmark import BenchmarkApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.models.general import BenchmarkReport
from scoremodel import db


class BenchmarkReportApi(GenericApi):
    simple_params = ['title', 'report_id']
    complex_params = []
    required_params = ['title', 'report_id']
    possible_params = simple_params + complex_params

    def create(self, object_data):
        cleaned_data = self.parse_input_data(object_data)
        existing_report = BenchmarkReport.query.filter(and_(BenchmarkReport.report_id == cleaned_data['report_id'],
                                                            BenchmarkReport.title == cleaned_data['title'])).first()
        if existing_report:
            raise DatabaseItemAlreadyExists(_e['item_already_in'].format(BenchmarkReport, cleaned_data['title'],
                                                                         'Report', cleaned_data['report_id']))
        new_report = BenchmarkReport(title=cleaned_data['title'])
        db.session.add(new_report)
        report = ReportApi().read(cleaned_data['report_id'])
        new_report.report = report
        db.session.commit()
        return new_report

    def read(self, object_id):
        existing_report = BenchmarkReport.query.filter(BenchmarkReport.id == object_id).first()
        if not existing_report:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(BenchmarkReport, object_id))
        return existing_report

    def update(self, object_id, object_data):
        existing_report = self.read(object_id)
        cleaned_data = self.parse_input_data(object_data)
        existing_report = self.update_simple_attributes(existing_report, self.simple_params, cleaned_data,
                                                        to_skip=['report_id'])
        db.session.commit()
        return existing_report

    def delete(self, object_id):
        existing_report = self.read(object_id)
        db.session.delete(existing_report)
        db.session.commit()
        return True

    def list(self):
        return []

    def parse_input_data(self, input_data):
        return self.clean_input_data(BenchmarkReport, input_data, self.possible_params, self.required_params,
                                     self.complex_params)
