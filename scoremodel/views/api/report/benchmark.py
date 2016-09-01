from flask import request
from flask.ext.login import login_required

from scoremodel.modules.api.rest.scoremodel import ScoremodelRestApi
from scoremodel.modules.api.benchmark.benchmark import BenchmarkApi
from scoremodel.modules.api.benchmark.rest_api import BenchmarkQueryRestApi
from scoremodel import csrf
from scoremodel.views.api import api


@api.route('/benchmark', methods=['POST'])
@api.route('/benchmark/<int:benchmark_id>', methods=['PUT', 'DELETE'])
@login_required
def v_api_benchmark(benchmark_id=None):
    a_api = ScoremodelRestApi(api_class=BenchmarkApi, o_request=request, api_obj_id=benchmark_id)
    return a_api.response


@csrf.exempt
@api.route('/benchmark_report/<int:benchmark_report_id>/question/<int:question_id>', methods=['GET'])
@login_required
def v_api_benchmark_report(benchmark_report_id, question_id):

    def hook_insert_ids(input_data):
        input_data['benchmark_report_id'] = benchmark_report_id
        input_data['question_id'] = question_id
        return input_data

    a_api = BenchmarkQueryRestApi(api_class=BenchmarkApi, o_request=request, hooks=[hook_insert_ids], api_obj_id='')
    return a_api.response


@csrf.exempt
@api.route('/benchmark', methods=['GET'])
@api.route('/benchmark/<int:benchmark_id>', methods=['GET'])
@login_required
def v_api_benchmark_get(benchmark_id=None):
    a_api = ScoremodelRestApi(api_class=BenchmarkApi, o_request=request, api_obj_id=benchmark_id)
    return a_api.response