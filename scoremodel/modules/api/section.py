from scoremodel.models.general import Question, Report, Section
from sqlalchemy import and_, or_
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
import scoremodel.modules.api.report
import scoremodel.modules.api.question
from scoremodel import db


class SectionApi(GenericApi):
    simple_params = ['title', 'context', 'total_score', 'order_in_report', 'report_id']
    complex_params = []

    ##
    # TODO auto-generate total_score from attached questions?
    ##

    def __init__(self, section_id=None):
        self.section_id = section_id
        self.a_report = scoremodel.modules.api.report.ReportApi()

    def create(self, input_data):
        """
        Create a new section. See QuestionApi.create(). Sections are in a report and have questions.
        :param input_data:
        :param report_id:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_section = Section.query.filter(and_(Section.title == cleaned_data['title'],
                                                     Section.report_id == cleaned_data['report_id'])).first()
        if existing_section is not None:
            raise DatabaseItemAlreadyExists('A section called "{0}" already exists in the report {1}'
                                            .format(cleaned_data['title'], cleaned_data['report_id']))
        new_section = Section(title=cleaned_data['title'], context=cleaned_data['context'],
                              total_score=cleaned_data['total_score'], order=cleaned_data['order_in_report'])
        db.session.add(new_section)
        db.session.commit()
        # Add to the report
        report = self.a_report.read(cleaned_data['report_id'])
        new_section.report = report
        db.session.commit()
        return new_section

    def read(self, section_id):
        """
        Return a section based on its id. See QuestionApi.read()
        :param section_id:
        :param section_data:
        :return:
        """
        existing_section = Section.query.filter(Section.id == section_id).first()
        if existing_section is None:
            raise DatabaseItemDoesNotExist('No section with id {0}'.format(section_id))
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
        existing_section = self.update_simple_attributes(existing_section, self.simple_params, cleaned_data)
        # Store
        db.session.commit()
        return existing_section

    def delete(self, section_id):
        """
        Delete an existing section. See QuestionApi.delete()
        :param section_id:
        :return:
        """
        existing_section = self.read(section_id)
        db.session.delete(existing_section)
        db.session.commit()
        return True

    def parse_input_data(self, input_data):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parameters have been filled. All missing parameters are set to None
        :param input_data:
        :return:
        """
        possible_params = ['title', 'context', 'total_score', 'order_in_report', 'report_id']
        required_params = ['title', 'total_score', 'report_id']
        cleaned_data = self.clean_input_data(Section, input_data, possible_params, required_params, self.complex_params)
        return cleaned_data

    def list(self):
        return []
