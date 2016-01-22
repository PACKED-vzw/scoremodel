from scoremodel import app
from flask import request, make_response, render_template, redirect, url_for, flash
from flask.ext.login import login_required
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.report.admin import ReportCreateForm, ReportDeleteForm
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist


@app.route('/admin/answer/list')
@login_required
@must_be_admin
def v_answer_list():
    pass


@app.route('/admin/answer/create')
@login_required
@must_be_admin
def v_answer_create():
    pass


@app.route('/admin/answer/edit/<int:answer_id>')
@login_required
@must_be_admin
def v_answer_edit(answer_id):
    pass


@app.route('/admin/answer/delete/<int:answer_id>')
@login_required
@must_be_admin
def v_answer_delete(answer_id):
    pass
