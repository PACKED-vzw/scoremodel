from flask import request, render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required, current_user

from scoremodel import app
from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing
from scoremodel.modules.forms.public.report import UserReportCreateForm

user_report_api = UserReportApi()


@app.route('/user/<int:user_id>/report', methods=['GET'])
@login_required
def v_user_report_list_by_user(user_id):
    if current_user.id != user_id:
        flash('You can only view your own reports.')
        abort(403)
    user_api = UserApi()
    reports_user = user_api.get_user_reports(user_id)
    return render_template('public/list.html', reports=reports_user, title='Rapporten')


@app.route('/user/<int:user_id>/report/new', methods=['GET', 'POST'])
@login_required
def v_user_report_new(user_id):
    if current_user.id != user_id:
        flash('You can only view your own reports.')
        abort(403)
    form = UserReportCreateForm()
    report_api = ReportApi()
    form.report.choices = [(r.id, r.title) for r in report_api.list()]
    if request.method == 'POST' and form.validate_on_submit():
        user_report_data = {
            'user_id': current_user.id,
            'report_id': form.report.data,
            'name': form.name.data
        }
        try:
            new_user_report = user_report_api.create(user_report_data)
        except DatabaseItemAlreadyExists as e:
            flash('This report already exists.')
            return redirect(url_for('.v_user_report_new', user_id=user_id))
        except RequiredAttributeMissing as e:
            flash('A required form element was not submitted: {0}'.format(e))
            return redirect(url_for('.v_user_report_new', user_id=current_user.id))
        except Exception as e:
            flash('An unexpected error occurred.')
            flash('The error is {0}'.format(e))
            return redirect(url_for('.v_user_report_new', user_id=current_user.id))
        else:
            report_api = ReportApi()
            report_template = report_api.read(new_user_report.report_id)
            first_section = report_template.ordered_sections[0]
            flash('Rapport aangemaakt.')
            return redirect(url_for('.v_user_report_section', report_id=new_user_report.id, user_id=current_user.id,
                                    section_id=first_section.id))
    else:
        return render_template('public/create.html', form=form, title='Nieuw rapport')


@app.route('/user/<int:user_id>/report/<int:report_id>', methods=['GET', 'POST'])
@login_required
def v_user_report_edit(user_id, report_id):
    if current_user.id != user_id:
        flash('You can only view your own reports.')
        abort(403)
    form = UserReportCreateForm()
    report_api = ReportApi()
    form.report.choices = [(r.id, r.title) for r in report_api.list()]
    try:
        existing_user_report = user_report_api.read(report_id)
    except DatabaseItemDoesNotExist as e:
        flash('This report does not exist.')
        return redirect(url_for('.v_user_report_list_by_user', user_id=current_user.id))
    except Exception as e:
        flash('An unexpected error occurred.')
        flash('{0}'.format(e))
        return redirect(url_for('.v_user_report_list_by_user', user_id=current_user.id))
    if request.method == 'POST' and form.validate_on_submit():
        input_data = {
            'user_id': current_user.id,
            'report_id': form.report.data,
            'name': form.name.data
        }
        if input_data['report_id'] != existing_user_report.id:
            # We have to delete all the QuestionAnswer's, as they are no longer current
            for question_answer in existing_user_report.question_answers:
                qa_api = QuestionAnswerApi()
                try:
                    qa_api.delete(question_answer.id)
                except Exception as e:
                    flash('An unexpected error occurred.')
                    flash('{0}'.format(e))
                    return redirect(url_for('.v_user_report_list_by_user', user_id=current_user.id))
        try:
            edited_user_report = user_report_api.update(existing_user_report.id, input_data)
        except RequiredAttributeMissing as e:
            flash('A required form element was not submitted: {0}'.format(e))
            return redirect(url_for('.v_user_report_edit', user_id=current_user.id, report_id=report_id))
        except Exception as e:
            flash('An unexpected error occurred.')
            flash(e)
            return redirect(url_for('.v_user_report_list_by_user', user_id=current_user.id))
        else:
            return redirect(url_for('.v_user_report_list_by_user', user_id=current_user.id))
    else:
        form.report.default = str(existing_user_report.report_id)
        form.name.default = existing_user_report.name
        form.process()
        return render_template('public/edit.html', form=form, title='Rapport bewerken', report_id=report_id)


@app.route('/user/<int:user_id>/report/<int:report_id>/section/<int:section_id>', methods=['GET'])
@login_required
def v_user_report_section(user_id, report_id, section_id):
    section_api = SectionApi()
    question_answer_api = QuestionAnswerApi()
    if current_user.id != user_id:
        flash('You can only view your own reports.')
        abort(403)
    try:
        user_report = user_report_api.read(report_id)
    except DatabaseItemDoesNotExist as e:
        flash('This page does not exist.')
        abort(404)
    except Exception as e:
        flash('An unexpected error occurred.')
        return redirect(url_for('.v_index'))
    # Get the sections that should be part of the report template. Check whether
    # section_id is part of them. If not, bail out.
    sections = user_report.template.sections
    if section_id not in [section.id for section in sections]:
        abort(404)
    current_section = section_api.read(section_id)
    return render_template('public/section.html', title=current_section.title, section=current_section,
                           report_id=report_id)


@app.route('/user/<int:user_id>/report/<int:report_id>/check', methods=['GET'])
@login_required
def v_user_report_check(user_id, report_id):
    if current_user.id != user_id:
        flash('You can only view your own reports.')
        abort(403)


@app.route('/user/<int:user_id>/report/<int:report_id>/print', methods=['GET'])
@login_required
def v_user_report_print(user_id, report_id):
    if current_user.id != user_id:
        flash('You can only view your own reports.')
        abort(403)
