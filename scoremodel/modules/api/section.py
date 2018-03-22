from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Question, Report, Section
from sqlalchemy import and_, or_
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
import scoremodel.modules.api.report
import scoremodel.modules.api.question
from scoremodel import db


class SectionApi(GenericApi):
    simple_params = ['title', 'context', 'order_in_report', 'report_id', 'weight']
    complex_params = []
    possible_params = ['title', 'context', 'order_in_report', 'report_id', 'weight']
    required_params = ['title', 'report_id']

    ##
    # TODO auto-generate total_score from attached questions?
    ##

    def __init__(self, section_id=None, autocommit=True):
        self.section_id = section_id
        self.a_report = scoremodel.modules.api.report.ReportApi()
        self.autocommit = autocommit

    def create(self, input_data):
        """
        Create a new section. See QuestionApi.create(). Sections are in a report and have questions.
        :param input_data:
        :param report_id:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        if self.db_exists(cleaned_data['title'], cleaned_data['report_id']):
            raise DatabaseItemAlreadyExists(_e['item_already_in']
                                            .format(Section, cleaned_data['title'], Report, cleaned_data['report_id']))
        return self.db_create(cleaned_data, self.a_report.read(cleaned_data['report_id']))

    def read(self, section_id):
        """
        Return a section based on its id. See QuestionApi.read()
        :param section_id:
        :param section_data:
        :return:
        """
        existing_section = Section.query.filter(Section.id == section_id).first()
        if existing_section is None:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Section, section_id))
        return existing_section

    def update(self, section_id, input_data):
        """
        Update an existing section. See QuestionApi.update()
        :param section_id:
        :param input_data:
        :param report_id:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_section = self.read(section_id)
        return self.db_update(existing_section, cleaned_data)

    def delete(self, section_id):
        """
        Delete an existing section. See QuestionApi.delete()
        :param section_id:
        :return:
        """
        existing_section = self.read(section_id)
        db.session.delete(existing_section)
        self.store()
        return True

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

    def list(self):
        return []

    def store(self):
        if self.autocommit:
            db.session.commit()

    def db_create(self, cleaned_data, report):
        """
        Create a section. This is a collection of all the write actions to the database, so we can wrap
        them in a transaction. We have to separate the "read" (query) actions as SQLAlchemy commits everything
        before querying (http://docs.sqlalchemy.org/en/latest/orm/session_basics.html).
        :param cleaned_data:
        :param report:
        :return:
        """
        new_section = Section(title=cleaned_data['title'], context=cleaned_data['context'],
                              order=cleaned_data['order_in_report'], weight=cleaned_data['weight'])
        db.session.add(new_section)
        # Add to the report
        new_section.report = report
        self.store()
        self.set_maximum_score(new_section.id)
        return new_section

    def db_update(self, existing_section, cleaned_data):
        """
        See self.db_create() on why this function exists.
        :param existing_section:
        :param cleaned_data:
        :return:
        """
        existing_section = self.update_simple_attributes(existing_section, self.simple_params, cleaned_data)
        # Store
        self.store()
        self.set_maximum_score(existing_section.id)
        return existing_section

    def db_exists(self, section_title, report_id):
        """

        :param section_title:
        :param report_id:
        :return:
        """
        existing_section = Section.query.filter(and_(Section.title == section_title,
                                                     Section.report_id == report_id)).first()
        if existing_section is not None:
            return True
        return False

    def total_score(self, section_id):
        """
        Get the total of the maximum score for each question in this section.
        :param section_id:
        :return:
        """
        existing_section = self.read(section_id)
        return existing_section.maximum_score

    def multiplication_factor(self, section_id):
        """
        Multiply each score (in question_answer) by this to get the result x/100
        :param section_id:
        :return:
        """
        total_score = self.total_score(section_id)
        if total_score == 0:
            return 100
        else:
            return 100 / total_score

    def set_maximum_score(self, section_id):
        """
        Set the maximum score for this section. This is defined as adding all the maximum scores of the dependent
        questions.
        :param section_id:
        :return:
        """
        existing_section = self.read(section_id)
        maximum = 0
        for question in existing_section.questions:
            maximum = maximum + scoremodel.modules.api.question.QuestionApi().maximum_score(question.id)
        existing_section.maximum_score = maximum
        self.store()
