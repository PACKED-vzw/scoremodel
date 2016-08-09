from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
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
        # A list of objects that have been created by this action.
        # This list will be deleted when an error occurs. We should be using transactions, but
        # in mysql you can't have transactions and foreign keys. We need the latter.
        # Note that updates to existing items will not be rolled back.
        question_api = QuestionApi(autocommit=False)
        section_api = SectionApi(autocommit=False)
        prepared_data = {
            'report': self.parse_input_data(report_data)
        }
        if 'sections' not in report_data:
            raise RequiredAttributeMissing(_e['attr_missing'].format('sections'))

        ##
        # Check the sections
        # 1) Check whether any new section has the same title as a section already in the DB
        # 2) Check whether any new section has a title equal to another section
        if 'id' in report_data and report_data['id'] > 0:
            # This report already exists, has an id and thus the sections can be tested for existence.
            # Otherwise, if it is a new report, they can't exist already (sections must be unique in a report)
            for unclean_section in report_data['sections']:
                clean_section = self.parse_input_data(unclean_section)
                if section_api.db_exists(clean_section['title'], report_data['id']):
                    raise DatabaseItemAlreadyExists(_e['item_already_in']
                                                    .format('Section', clean_section['title'], report_data['id']))
        # Check for duplicate sections
        counted = {}
        for item in report_data['sections']:
            if item['title'] in counted:
                counted[item['title']] = + 1
                raise DatabaseItemAlreadyExists(_('Error: duplicate section title {0}').format(item['title']))
            else:
                counted[item['title']] = 1

        ##
        # Check the questions
        # 1) Check whether any new question has the same title ("question") as one already in the DB
        # 2) Check whether any new question has a title equal to another question
        for section in report_data['sections']:
            if 'questions' not in section:
                raise RequiredAttributeMissing(_e['attr_missing'].format('questions'))
            if 'id' in section and section['id'] > 0:
                for question in section['questions']:
                    clean_question = question_api.parse_input_data(question)
                    if question_api.db_exists(clean_question['question'], section['id']):
                        raise DatabaseItemAlreadyExists(_e['item_already_in']
                                                    .format('Question', clean_question['question'], section['id']))
            # Check for duplicate questions
            counted = {}
            for item in section['questions']:
                if item['question'] in counted:
                    counted[item['question']] = + 1
                    raise DatabaseItemAlreadyExists(_('Error: duplicate question {0}').format(item['question']))
                else:
                    counted[item['question']] = 1


        ##
        # Start the transaction
        # 1) Add the report
        # 2) Add any new section and update existing ones
        # 3) Add any new questions and update existing ones
        # -> rollback when something goes wrong + raise the error
        # begin transaction
        db.session.begin(subtransactions=True)
        # switch off autocommit

        # The create function of ReportApi will strip all attributes that are not
        # defined in the DB. So we store this one to prevent it from being lost.
        unclean_sections = report_data['sections']
        clean_report_data = self.parse_input_data(report_data)
        created_report = self.db_create(clean_report_data, False)

        for unclean_section in unclean_sections:
            unclean_questions = unclean_section['questions']
            unclean_section['report_id'] = created_report.id
            clean_section = section_api.parse_input_data(unclean_section)
            # Problem with updates
            created_section = self.add_section(clean_section, created_report)
            for unclean_question in unclean_questions:
                unclean_question['section_id'] = created_section.id
                clean_question = question_api.parse_input_data(unclean_question)

        # Commit
        db.session.commit()

        return created_report

    def update(self, report_id, input_data, autocommit=False):
        existing_report = self.read(report_id)

        if 'sections' not in input_data:
            raise RequiredAttributeMissing(_e['attr_missing'].format('sections'))
        sections = input_data['sections']

        # start transaction
        db.session.begin(subtransactions=True)
        section_api = SectionApi(autocommit=False)
        question_api = QuestionApi(autocommit=False)

        existing_report = super(ReportCreateApi, self).update(report_id, input_data, autocommit=False)

        # Remove all sections in existing_report that are not part of input_data['sections']
        # Sections (and questions) cannot exist if they are not part of a report
        for section in existing_report.sections:
            if section.id not in [s['id'] for s in sections]:
                section_api.delete(section.id)

        for new_section in sections:
            new_section['report_id'] = existing_report.id
            questions = new_section['questions']

            existing_section = self.add_section(new_section)

            for question in existing_section.questions:
                if question.id not in [q['id'] for q in questions]:
                    question_api.delete(question.id)

            for new_question in questions:
                new_question['section_id'] = existing_section.id

                existing_question = self.add_question(new_question)

        # Commit
        db.session.commit()

        return existing_report

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
