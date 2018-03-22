from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.public import UserReport, QuestionAnswer
from scoremodel.models.general import Report, Section
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.benchmark.report import BenchmarkReportApi
from scoremodel import db
import datetime


class UserReportApi(GenericApi):
    simple_params = ['name', 'user_id', 'report_id', 'creation_time', 'last_modified']
    complex_params = []
    required_params = ['name', 'user_id', 'report_id']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        new_user_report = UserReport(name=cleaned_data['name'], user_id=cleaned_data['user_id'],
                                     report_id=cleaned_data['report_id'])
        db.session.add(new_user_report)
        db.session.commit()
        return new_user_report

    def read(self, report_id):
        existing_user_report = UserReport.query.filter(UserReport.id == report_id).first()
        if existing_user_report is None:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(UserReport, report_id))
        return existing_user_report

    def update(self, report_id, input_data):
        cleaned_data = self.parse_input_data(input_data)
        existing_user_report = self.read(report_id)
        if 'creation_time' not in cleaned_data or cleaned_data['creation_time'] is None:
            cleaned_data['creation_time'] = existing_user_report.creation_time
            if cleaned_data['creation_time'] is None:
                cleaned_data['creation_time'] = datetime.datetime.now()
        cleaned_data['last_modified'] = datetime.datetime.now()
        existing_user_report = self.update_simple_attributes(existing_user_report, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_user_report

    def delete(self, report_id):
        existing_user_report = self.read(report_id)
        db.session.delete(existing_user_report)
        db.session.commit()
        return True

    def list(self):
        existing_reports = UserReport.query.all()
        return existing_reports

    def parse_input_data(self, input_data):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parameters have been filled. All missing parameters are set to None
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input_data(Section, input_data, self.possible_params, self.required_params,
                                             self.complex_params)
        return cleaned_data

    def benchmarks_by_section(self, user_report_id):
        """
        Get all benchmark questions (grouped per report) per section.
        :param user_report_id:
        :return:
        """
        bm_by_section = {}
        benchmark_report_api = BenchmarkReportApi()
        existing_user_report = self.read(user_report_id)
        for benchmark_report in existing_user_report.template.benchmark_reports:
            benchmark_questions_by_section = benchmark_report_api.questions_by_section(benchmark_report.id)
            for section_id, benchmarks in benchmark_questions_by_section.items():
                section_score = 0
                multiplication_factor = SectionApi().multiplication_factor(section_id)
                for benchmark in benchmarks:
                    section_score += benchmark.score * multiplication_factor
                if section_id in bm_by_section:
                    if benchmark_report.id in bm_by_section[section_id]:
                        raise Exception(_('Multiple values for the same benchmark_report in the same section.'))
                    else:
                        bm_by_section[section_id][benchmark_report.id] = {
                            'title': benchmark_report.title,
                            'section_score': section_score,
                            'benchmarks': {b.question_id: b for b in benchmark_questions_by_section[section_id]}
                        }
                else:
                    bm_by_section[section_id] = {
                        benchmark_report.id: {
                            'title': benchmark_report.title,
                            'section_score': section_score,
                            'benchmarks': {b.question_id: b for b in benchmark_questions_by_section[section_id]}
                        }
                    }
        return bm_by_section
