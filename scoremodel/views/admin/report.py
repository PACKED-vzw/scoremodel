from scoremodel.views.admin import admin
from flask import request, make_response, render_template, redirect, url_for, flash
from flask_login import login_required
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.locale import Locale
from scoremodel.modules.forms.generic import GenericDeleteForm
from scoremodel.modules.api.benchmark.benchmark import BenchmarkApi
from scoremodel.modules.api.benchmark.report import BenchmarkReportApi
from scoremodel.modules.report.admin import ReportCreateForm, ReportDeleteForm
from scoremodel.modules.forms.benchmark_report import BenchmarkReportCreateForm
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist
from flask_babel import gettext as _

lang_api = LangApi()
locale_api = Locale()


@admin.route('/reports', methods=['GET'])
@login_required
@must_be_admin
def v_report_list():
    a_report = ReportApi()
    l_reports = a_report.list()
    return render_template('admin/report/list.html', reports=l_reports)


@admin.route('/reports/id/<int:report_id>/edit', methods=['GET'])
@login_required
@must_be_admin
def v_report_edit(report_id):
    a_report = ReportApi()
    a_answer = AnswerApi()
    a_risk_factor = RiskFactorApi()
    a_lang = LangApi()
    try:
        existing_report = a_report.read(report_id)
    except DatabaseItemDoesNotExist:
        flash(_('No report with id {0} exists.').format(report_id))
        return redirect(url_for('admin.v_report_list'))
    # Do not use fallback_locale for the answers and risk_factor choices: if they don't exist, the administrator
    # must create them.
    report_lang = a_lang.read(existing_report.lang_id)
    return render_template('admin/report/edit.html', report=existing_report,
                           all_risk_factors=a_risk_factor.by_lang(report_lang.lang),
                           all_answers=a_answer.by_lang(report_lang.lang), languages=lang_api.list())


@admin.route('/reports/id/<int:report_id>/delete', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_report_delete(report_id):
    form = ReportDeleteForm()
    a_report = ReportApi()
    try:
        existing_report = a_report.read(report_id)
    except DatabaseItemDoesNotExist:
        flash(_('No report with id {0} exists.').format(report_id))
        return url_for('admin.v_report_list')
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if a_report.delete(report_id) is True:
                flash(_('Report {0} removed.').format(report_id))
            else:
                flash(_('Failed to remove report {0}.').format(report_id))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return render_template('admin/generic/delete.html', action_url=url_for('admin.v_report_delete',
                                                                                   report_id=report_id),
                                   item_type=_('Report'), item_identifier=existing_report.title, form=form)
        else:
            return redirect(url_for('admin.v_report_list'))
    return render_template('admin/generic/delete.html', action_url=url_for('admin.v_report_delete',
                                                                           report_id=report_id),
                           item_type=_('Report'), item_identifier=existing_report.title, form=form)


@admin.route('/reports/create', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_report_create():
    form = ReportCreateForm()
    form.lang.choices = [(l.id, l.lang) for l in lang_api.list()]
    if request.method == 'POST' and form.validate_on_submit():
        a_report = ReportApi()
        input_data = {
            'title': form.title.data,
            'lang_id': form.lang.data
        }
        try:
            new_report = a_report.create(input_data)
        except DatabaseItemAlreadyExists as e:
            flash(_('A report called {0} already exists.').format(input_data['title']))
            return render_template('admin/report/create.html', form=form)
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
            return render_template('admin/report/create.html', form=form)
        except Exception as e:  # Remove this after debugging
            #    flash('An unexpected error occurred: {0}'.format(e))
            flash(_('An unexpected error occurred.'))
            return render_template('admin/report/create.html', form=form)
        else:
            flash(_('Report created.'))
            return redirect(url_for('admin.v_report_edit', report_id=new_report.id))
    return render_template('admin/report/create.html', form=form)


@admin.route('/reports/benchmark', methods=['GET'])
@login_required
@must_be_admin
def v_report_benchmark_report():
    return render_template('admin/report/benchmark/list.html', benchmarks=BenchmarkReportApi().list())


@admin.route('/reports/benchmark/create', methods=['GET', 'POST'])
@admin.route('/reports/benchmark/create/report/<int:report_id>', methods=['GET'])
@login_required
@must_be_admin
def v_report_benchmark_create(report_id=None):
    form = BenchmarkReportCreateForm()
    report_api = ReportApi()
    benchmark_report_api = BenchmarkReportApi()
    choices = [(r.id, r.title) for r in report_api.list()]
    form.report.choices = choices
    if report_id:
        form.report.data = report_id
    if request.method == 'POST' and form.validate_on_submit():
        benchmark_report_data = {
            'title': form.name.data,
            'report_id': form.report.data
        }
        try:
            new_benchmark_report = benchmark_report_api.create(benchmark_report_data)
        except DatabaseItemAlreadyExists as e:
            flash(_('This report already exists.'))
            return redirect(url_for('admin.v_report_benchmark_create'))
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
            return redirect(url_for('admin.v_report_benchmark_create'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('admin.v_report_benchmark_create'))
        else:
            flash('Benchmark created')
            return redirect(url_for('admin.v_report_benchmark_edit', benchmark_report_id=new_benchmark_report.id))
    else:
        return render_template('admin/report/benchmark/create.html', form=form, title=_('New benchmark'))


@admin.route('/reports/benchmark/<int:benchmark_report_id>/delete', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_report_benchmark_delete(benchmark_report_id):
    form = GenericDeleteForm()
    benchmark_report_api = BenchmarkReportApi()
    try:
        existing_benchmark_report = benchmark_report_api.read(benchmark_report_id)
    except DatabaseItemDoesNotExist:
        flash(_('No benchmark report with id {0} exists.').format(benchmark_report_id))
        return url_for('admin.v_report_benchmark_report')
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if benchmark_report_api.delete(benchmark_report_id) is True:
                flash(_('Benchmark report {0} removed.').format(benchmark_report_id))
            else:
                flash(_('Failed to remove benchmark report {0}.').format(benchmark_report_id))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return render_template('admin/generic/delete.html', action_url=url_for('admin.v_report_benchmark_delete',
                                                                                   benchmark_report_id=benchmark_report_id),
                                   item_type=_('Benchmark eport'), item_identifier=existing_benchmark_report.title, form=form)
        else:
            return redirect(url_for('admin.v_report_benchmark_report'))
    return render_template('admin/generic/delete.html', action_url=url_for('admin.v_report_benchmark_delete',
                                                                                   benchmark_report_id=benchmark_report_id),
                                   item_type=_('Benchmark eport'), item_identifier=existing_benchmark_report.title, form=form)


@admin.route('/reports/benchmark/<int:benchmark_report_id>/edit', methods=['GET'])
@login_required
@must_be_admin
def v_report_benchmark_edit(benchmark_report_id):
    benchmark_report = BenchmarkReportApi().read(benchmark_report_id)
    benchmarks = BenchmarkApi().by_benchmark_report_id(benchmark_report_id)
    ordered_benchmarks = {}
    for benchmark in benchmarks:
        ordered_benchmarks[benchmark.question_id] = benchmark
    return render_template('admin/report/benchmark/edit.html', benchmark_report_id=benchmark_report_id,
                           benchmark_report=benchmark_report, benchmarks=ordered_benchmarks)


##
# Helpers (TODO?)
##
