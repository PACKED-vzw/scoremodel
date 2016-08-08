from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import Report
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel import db


##
# TODO: rollback
# https://dev.mysql.com/doc/refman/5.7/en/ansi-diff-foreign-keys.html
# cascade rollback?
# TODO: implement this
# disable foreign keys check -> <transaction> -> commit -> enable foreign keys check


class ReportCreateApi(ReportApi):

    def create(self, input_data):
        """
        Create a report, but with all sections and questions attached.
        Every section/question has an id. If it is negative, we consider
        it to be a new section/question. Otherwise, we update.
        (implement rollback??) TODO
        :param input_data:
        :return:
        """
        # A list of objects that have been created by this action.
        # This list will be deleted when an error occurs. We should be using transactions, but
        # in mysql you can't have transactions and foreign keys. We need the latter.
        # Note that updates to existing items will not be rolled back.
        if 'sections' not in input_data:
            self.rollback()
            raise RequiredAttributeMissing(_e['attr_missing'].format('sections'))

        # The create function of ReportApi will strip all attributes that are not
        # defined in the DB. So we store this one to prevent it from being lost.
        sections = input_data['sections']

        existing_report = super(ReportCreateApi, self).create(input_data)
        self.created.append(existing_report)

        for section in sections:
            if 'questions' not in section:
                self.rollback()
                raise RequiredAttributeMissing(_e['attr_missing'].format('questions'))

            questions = section['questions']

            section['report_id'] = existing_report.id
            existing_section = self.add_section(section)
            for question in questions:
                question['section_id'] = existing_section.id
                existing_question = self.add_question(question)

        return existing_report

    def update(self, report_id, input_data):
        existing_report = self.read(report_id)

        if 'sections' not in input_data:
            raise RequiredAttributeMissing(_e['attr_missing'].format('sections'))
        sections = input_data['sections']

        section_api = SectionApi()
        question_api = QuestionApi()

        existing_report = super(ReportCreateApi, self).update(report_id, input_data)

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

        return existing_report

    def add_question(self, question_data):
        question_api = QuestionApi()
        if 'id' in question_data and question_data['id'] > 0:
            # Update
            try:
                existing_question = question_api.update(question_data['id'], question_data)
            except Exception as e:
                self.rollback()
                raise e
        else:
            try:
                existing_question = question_api.create(question_data)
            except Exception as e:
                self.rollback()
                raise e
            self.created.append(existing_question)
        return existing_question

    def add_section(self, section_data):
        section_api = SectionApi()
        if 'id' in section_data and section_data['id'] > 0:
            # Update
            try:
                existing_section = section_api.update(section_data['id'], section_data)
            except Exception as e:
                self.rollback()
                raise e
        else:
            # Create
            try:
                existing_section = section_api.create(section_data)
            except Exception as e:
                self.rollback()
                raise e
            self.created.append(existing_section)
        return existing_section

    def generic_delete(self, database_object):
        db.session.delete(database_object)
        db.session.commit()
        return True

    def rollback(self):
        for c in self.created:
            self.generic_delete(c)
