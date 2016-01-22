from scoremodel import app
from flask import request, make_response, render_template, redirect, url_for, flash
from flask.ext.login import login_required
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.report.admin import ReportCreateForm, ReportDeleteForm
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist


@app.route('/admin/risk_factor/list')
@login_required
@must_be_admin
def v_risk_factor_list():
    pass


@app.route('/admin/risk_factor/create')
@login_required
@must_be_admin
def v_risk_factor_create():
    pass


@app.route('/admin/risk_factor/edit/<int:risk_factor_id>')
@login_required
@must_be_admin
def v_risk_factor_edit(risk_factor_id):
    pass


@app.route('/admin/risk_factor/delete/<int:risk_factor_id>')
@login_required
@must_be_admin
def v_risk_factor_delete(risk_factor_id):
    pass
