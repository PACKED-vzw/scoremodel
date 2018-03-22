from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Report
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel import db
from flask_babel import lazy_gettext as _


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

    def store_chain(self, report_data, created_report):
        """
        For an already stored report (created_report), store all sections
        and attached questions in the DB. Will automatically distinguish between
        new sections/questions and updated sections/questions.
        :param report_data:
        :param created_report:
        :return:
        """
        section_api = SectionApi()
        question_api = QuestionApi()
        # Check for sections that were originally part of created_report, but are not anymore
        # We delete those.
        original_sections = created_report.sections
        new_sections = []
        for s in report_data['sections']:
            if 'id' in s:
                new_sections.append(s)
        #for original_section in original_sections:
        #    if original_section.id not in new_sections:
        #        section_api.delete(original_section.id)

        for section in report_data['sections']:
            section['report_id'] = created_report.id
            if 'id' in section and section['id'] > 0:
                # An update
                created_section = section_api.update(section['id'], section)
            else:
                # A new creation
                created_section = section_api.create(section)
            original_questions = created_section.questions
            new_questions = []
            for q in section['questions']:
                if 'id' in q:
                    new_questions.append(q)
            #for original_question in original_questions:
            #    if original_question.id not in new_questions:
            #        question_api.delete(original_question.id)
            for question in section['questions']:
                question['section_id'] = created_section.id
                if 'id' in question and question['id'] > 0:
                    # An update
                    created_question = question_api.update(question['id'], question)
                else:
                    # A new creation
                    created_question = question_api.create(question)
        return created_report

    def create(self, input_data):
        """
        Create a report, but with all sections and questions attached.
        Every section/question has an id. If it is negative, we consider
        it to be a new section/question. Otherwise, we update.
        :param input_data:
        :return:
        """
        # We're now simply going to add report, section and question using the default api functions.
        # While we should be using transactions, so we can roll back when an error occurs, we can't.
        # SQLAlchemy flushes all pending commits when a read query is executed, and the API requires
        # a lot of read queries (error checking, answer getting etc.). While we can get rid of some
        # we still need others. Furthermore, MySQL does not defer checking foreign keys until the
        # transaction has been committed. So to store sections, we first have to commit the report.
        # Otherwise, the foreign keys won't match. As this defeats the entire purpose of wrapping
        # everything in a transaction, we use self.check_error() to check for input errors. It will
        # bail out before it commits if there is one. All other errors will still result in inconsistent
        # data. So this is a TODO.
        if self.error_check(input_data) is not True:
            raise Exception(_e('An unexpected error occurred.'))
        if 'id' in input_data and input_data['id'] > 0:
            # This is an update
            return self.update(input_data['id'], input_data)
        created_report = super(ReportCreateApi, self).create(input_data)
        return self.store_chain(input_data, created_report)

    def update(self, report_id, input_data):
        """
        Update an existing report.
        :param report_id:
        :param input_data:
        :return:
        """
        input_data['id'] = report_id
        if self.error_check(input_data) is not True:
            raise Exception(_e('An unexpected error occurred.'))
        updated_report = super(ReportCreateApi, self).update(report_id, input_data)
        return self.store_chain(input_data, updated_report)
