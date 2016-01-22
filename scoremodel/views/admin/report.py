from scoremodel import app
from flask import request, make_response, render_template, redirect, url_for, flash
from flask.ext.login import login_required
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.report.admin import ReportCreateForm, ReportDeleteForm
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist


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


@app.route('/admin/reports/id/<int:report_id>/delete', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_report_delete(report_id):
    form = ReportDeleteForm()
    a_report = ReportApi()
    try:
        existing_report = a_report.read(report_id)
    except DatabaseItemDoesNotExist:
        flash('No report with id {0} exists.'.format(report_id))
        return url_for('.v_report_list')
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if a_report.delete(report_id) is True:
                flash('Report {0} removed.'.format(report_id))
            else:
                flash('Failed to remove report {0}.'.format(report_id))
        except Exception as e:
            flash('An unexpected error occurred.')
            return render_template('admin/generic/delete.html', action_url=url_for('.v_report_delete',
                                                                                   report_id=report_id),
                                   item_type='Report', item_identifier=existing_report.title, form=form)
        else:
            return redirect(url_for('.v_report_list'))
    return render_template('admin/generic/delete.html', action_url=url_for('.v_report_delete',
                                                                           report_id=report_id),
                           item_type='Report', item_identifier=existing_report.title, form=form)


@app.route('/admin/reports/create', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_report_create():
    form = ReportCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        a_report = ReportApi()
        input_data = {
            'title': form.title.data
        }
        try:
            new_report = a_report.create(input_data)
        except DatabaseItemAlreadyExists as e:
            flash('A report called {0} already exists.'.format(input_data['title']))
            return render_template('admin/report/create.html', form=form)
        except RequiredAttributeMissing as e:
            flash('A required form element was not submitted: {0}'.format(e))
            return render_template('admin/report/create.html', form=form)
        except Exception as e:  # Remove this after debugging
        #    flash('An unexpected error occurred: {0}'.format(e))
            flash('An unexpected error occurred.')
            return render_template('admin/report/create.html', form=form)
        else:
            flash('Report created.')
            return redirect(url_for('.v_report_edit', report_id=new_report.id))
    return render_template('admin/report/create.html', form=form)

##
# Helpers (TODO?)
##
