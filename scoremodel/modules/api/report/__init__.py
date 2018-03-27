from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Report
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.lang import LangApi
import scoremodel.modules.api.question
from scoremodel import db


class ReportApi(GenericApi):
    simple_params = ['title', 'lang_id']
    complex_params = []
    possible_params = ['title', 'lang_id']
    required_params = ['title', 'lang_id']

    def __init__(self, report_id=None, autocommit=True):
        self.report_id = report_id
        self.lang_api = LangApi()
        self.autocommit = autocommit

    def create(self, input_data):
        """
        Create a new report. See QuestionApi.create()
        :param input_data:
        :param autocommit:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        if self.db_exists(cleaned_data['title']):
            raise DatabaseItemAlreadyExists(_e['item_exists'].format(Report, cleaned_data['title']))
        return self.db_create(cleaned_data)

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
        :param autocommit:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_report = self.read(report_id)
        return self.db_update(existing_report, cleaned_data)

    def delete(self, report_id, autocommit=None):
        """
        Delete an existing report. See QuestionApi.delete()
        :param report_id:
        :param autocommit:
        :return:
        """
        existing_report = self.read(report_id)
        db.session.delete(existing_report)
        self.store(autocommit)
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
        return self.clean_input_data(Report, input_data, self.possible_params, self.required_params,
                                     self.complex_params)

    def store(self, autocommit=None):
        if autocommit is None:
            autocommit = self.autocommit
        if autocommit:
            db.session.commit()

    def db_exists(self, report_title):
        """
        If an item with this title already exists, return True. Else, return False.
        :param report_title:
        :return:
        """
        existing_report = Report.query.filter(Report.title == report_title).first()
        if existing_report is not None:
            return True
        return False

    def db_create(self, cleaned_data, autocommit=True):
        """
        Create a report. This is a collection of all the write actions to the database, so we can wrap
        them in a transaction. We have to separate the "read" (query) actions as SQLAlchemy commits everything
        before querying (http://docs.sqlalchemy.org/en/latest/orm/session_basics.html).
        :param cleaned_data:
        :param autocommit:
        :return:
        """
        new_report = Report(title=cleaned_data['title'], lang_id=cleaned_data['lang_id'])
        db.session.add(new_report)
        self.store(autocommit)
        return new_report

    def db_update(self, existing_report, cleaned_data, autocommit=True):
        """
        See self.db_create()
        :param existing_report:
        :param cleaned_data:
        :param autocommit:
        :return:
        """
        existing_report = self.update_simple_attributes(existing_report, simple_attributes=self.simple_params,
                                                        cleaned_data=cleaned_data)
        self.store(autocommit)
        return existing_report

    def questions_by_combined_weight(self, report_id):
        existing_report = self.read(report_id)
        unordered_questions = []
        for section in existing_report.sections:
            for question in section.questions:
                unordered_questions.append({
                    'question_id': question.id,
                    'combined_weight': question.risk_factor.value * question.weight * section.weight,
                    'max_score': scoremodel.modules.api.question.QuestionApi().maximum_score(question.id)
                })
        return sorted(unordered_questions, key=lambda q: q['combined_weight'], reverse=True)
