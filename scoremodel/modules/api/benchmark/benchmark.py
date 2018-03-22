from flask_babel import gettext as _
from sqlalchemy import and_
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.benchmark.report import BenchmarkReportApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.models.general import Benchmark
from scoremodel import db


class BenchmarkApi(GenericApi):
    simple_params = ['question_id', 'answer_id', 'benchmark_report_id']
    complex_params = []
    required_params = ['question_id', 'benchmark_report_id']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        cleaned_data = self.parse_input_data(input_data)

        existing_benchmark = Benchmark.query.filter(and_(Benchmark.question_id == cleaned_data['question_id'],
                                                         Benchmark.benchmark_report_id == cleaned_data[
                                                             'benchmark_report_id'])).first()
        if existing_benchmark:
            raise DatabaseItemAlreadyExists(
                _e['item_already_in'].format('Benchmark', existing_benchmark.id, 'BenchmarkReport',
                                             cleaned_data['benchmark_report_id']))
        new_benchmark = Benchmark()
        question = QuestionApi().read(cleaned_data['question_id'])
        benchmark_report = BenchmarkReportApi().read(cleaned_data['benchmark_report_id'])

        db.session.add(new_benchmark)
        new_benchmark.question = question
        if cleaned_data['answer_id']:
            answer = AnswerApi().read(cleaned_data['answer_id'])
            new_benchmark.answer = answer
        else:
            new_benchmark.not_in_benchmark = True
        new_benchmark.benchmark_report = benchmark_report
        db.session.commit()
        return new_benchmark

    def read(self, object_id):
        existing_benchmark = Benchmark.query.filter(Benchmark.id == object_id).first()
        if not existing_benchmark:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Benchmark, object_id))
        return existing_benchmark

    def update(self, object_id, input_data):
        """
        Updating makes no sense - delete and create a new one
        :param object_id:
        :param input_data:
        :return:
        """
        if self.delete(object_id):
            return self.create(input_data)
        else:
            raise Exception('An unexpected error occurred while updating a benchmark.')

    def delete(self, object_id):
        existing_benchmark = self.read(object_id)
        db.session.delete(existing_benchmark)
        db.session.commit()
        return True

    def list(self):
        return []

    def by_benchmark_report_id(self, benchmark_report_id):
        return Benchmark.query.filter(Benchmark.benchmark_report_id == benchmark_report_id).all()

    def query(self, input_data):
        cleaned_data = self.parse_input_data(input_data)
        existing_benchmark = Benchmark.query.filter(and_(
            Benchmark.benchmark_report_id == cleaned_data['benchmark_report_id'],
            Benchmark.question_id == cleaned_data['question_id']
        )).first()
        if not existing_benchmark:
            raise DatabaseItemDoesNotExist(_('No benchmark with benchmark_report_id {0} and question_id {1}.').format(
                cleaned_data['benchmark_report_id'],
                cleaned_data['question_id']
            ))
        return existing_benchmark

    def parse_input_data(self, input_data):
        return self.clean_input_data(Benchmark, input_data, self.possible_params, self.required_params,
                                     self.complex_params)
