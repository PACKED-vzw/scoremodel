from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Report
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel import db
from flask.ext.babel import lazy_gettext as _


##
# TODO: rollback
# https://dev.mysql.com/doc/refman/5.7/en/ansi-diff-foreign-keys.html
# cascade rollback?
# TODO: implement this
# disable foreign keys check -> <transaction> -> commit -> enable foreign keys check


class ReportCreateApi(ReportApi):

    def db_check(self, report_data):
        """
        For a report, check that reports, sections and questions do not already exist
        in the database when they are new.
        :param report_data:
        :return:
        """
        section_api = SectionApi(autocommit=False)
        question_api = QuestionApi(autocommit=False)
        if 'sections' not in report_data:
            raise RequiredAttributeMissing(_e['attr_missing'].format('sections'))
        if 'id' in report_data and report_data['id'] > 0:
            # Check the DB
            for section in report_data['sections']:
                # If there is no title, this will be caught by the other error checking routines
                if 'title' in section:
                    if 'id' not in section or section['id'] < 0:
                        if section_api.db_exists(section['title'], report_data['id']):
                            raise DatabaseItemAlreadyExists(_e['item_already_in'].format('Section', section['title'],
                                                                                         'Report', report_data['id']))
                if 'id' in section and section['id'] > 0:
                    # No sense in checking for questions in a section that doesn't exist
                    if 'questions' not in section:
                        raise RequiredAttributeMissing(_e['attr_missing'].format('questions'))
                    for question in section['questions']:
                        if 'question' in question:
                            if 'id' not in question or question['id'] < 0 :
                                if question_api.db_exists(question['question'], section['id']):
                                    raise DatabaseItemAlreadyExists(
                                        _e['item_already_in'].format('Question', question['question'],
                                                                     'Section', section['id']))
        return True

    def error_check(self, report_data):
        """
        Check all input for errors. The called functions will throw exceptions
        themselves. We are not trying to catch them, but to trigger them before
        we try to commit everything to the DB. This should prevent inconsistent data
        in the DB.
        :param report_data:
        :return:
        """
        section_api = SectionApi(autocommit=False)
        question_api = QuestionApi(autocommit=False)
        risk_factor_api = RiskFactorApi()

        # Database check
        if self.db_check(report_data) is not True:
            raise Exception(_('An unexpected error occurred.'))

        # Check for attributes
        if 'sections' not in report_data:
            raise RequiredAttributeMissing(_e['attr_missing'].format('sections'))
        cleaned_report = self.parse_input_data(report_data)

        # Check for duplicates (two sections with the same title)
        duplicate_sections = []
        for section in report_data['sections']:
            if 'questions' not in section:
                raise RequiredAttributeMissing(_e['attr_missing'].format('questions'))

            # Check for attributes
            cleaned_section = section_api.parse_input_data(section)
            # Duplicate check
            if section['title'] not in duplicate_sections:
                duplicate_sections.append(section['title'])
            else:
                raise DatabaseItemAlreadyExists(_e['item_already_in'].format('Section', section['title'],
                                                                             'Report', report_data['id']))

            duplicate_questions = []
            for question in section['questions']:
                # Check for attributes
                cleaned_question = question_api.parse_input_data(question)
                # Check for duplicates
                if question['question'] not in duplicate_questions:
                    duplicate_questions.append(question['question'])
                else:
                    raise DatabaseItemAlreadyExists(
                        _e['item_already_in'].format('Question', question['question'],
                                                     'Section', section['id']))
                # Check for answers
                # We must use the cleaned data, because 'answers' is not required,
                # and attempting to loop over None gets an error.
                for answer_id in cleaned_question['answers']:
                    answer = question_api.get_answer(answer_id)
                # Check for risk_factor
                risk_factor = risk_factor_api.read(cleaned_question['risk_factor_id'])
        return True

    def create(self, report_data, autocommit=False):
        """
        Create a report, but with all sections and questions attached.
        Every section/question has an id. If it is negative, we consider
        it to be a new section/question. Otherwise, we update.
        (implement rollback??) TODO
        :param report_data:
        :param autocommit:
        :return:
        """
        pass

    def update(self, report_id, input_data, autocommit=False):
        pass

    def add_question(self, question_data):
        question_api = QuestionApi()
        cleaned_data = question_api.parse_input_data(question_data)
        if 'id' in question_data and question_data['id'] > 0:
            # Update
            try:
                #existing_question = question_api.update(question_data['id'], question_data)
                existing_question = question_api.db_update('', cleaned_data)
            except Exception as e:
                self.rollback()
                raise e
        else:
            try:
                existing_question = question_api.create(question_data)
            except Exception as e:
                self.rollback()
                raise e
        return existing_question

    def add_section(self, section_data, report, section=None):
        section_api = SectionApi()
        if 'id' in section_data and section_data['id'] > 0:
            # Update
            try:
                existing_section = section_api.db_update(section, section_data)
            except Exception as e:
                self.rollback()
                raise e
        else:
            # Create
            try:
                existing_section = section_api.db_create(section_data, report)
            except Exception as e:
                self.rollback()
                raise e
        return existing_section

    def generic_delete(self, database_object):
        db.session.delete(database_object)
        return True

    def rollback(self):
        db.session.rollback()
