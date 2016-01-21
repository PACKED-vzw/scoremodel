from scoremodel import app
from flask import request, make_response, render_template
from flask.ext.login import login_required
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.api.report import ReportApi


@app.route('/admin/reports', methods=['GET'])
@login_required
@must_be_admin
def v_report_list():
    a_report = ReportApi()
    l_reports = a_report.list()
    return render_template('admin/report/list.html', reports=l_reports)


@app.route('/admin/reports/id/<int:report_id>/edit', methods=['GET'])
@login_required
@must_be_admin
def v_report_edit(report_id):
    return render_template('admin/report/edit.html', report_id=report_id)


@app.route('/admin/reports/id/<int:report_id>/delete', methods=['GET'])
@login_required
@must_be_admin
def v_report_delete(report_id):
    return ''

##
# Helpers (TODO?)
##
