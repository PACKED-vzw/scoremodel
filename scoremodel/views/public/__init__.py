from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing
from scoremodel.modules.forms.public.report import UserReportCreateForm

public = Blueprint('public', __name__, url_prefix='/scoremodel')

user_report_api = UserReportApi()


@public.route('', methods=['GET'])
@login_required
def v_index():
    return redirect(url_for('public.v_user_report_list_by_user', user_id=current_user.id))


@public.route('/user/<int:user_id>/report', methods=['GET'])
@login_required
def v_user_report_list_by_user(user_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
    user_api = UserApi()
    reports_user = user_api.get_user_reports(user_id)
    return render_template('public/list.html', reports=reports_user, title=_('Reports'))


@public.route('/user/<int:user_id>/report/new', methods=['GET', 'POST'])
@login_required
def v_user_report_new(user_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
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
            flash(_('This report already exists.'))
            return redirect(url_for('public.v_user_report_new', user_id=user_id))
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
            return redirect(url_for('public.v_user_report_new', user_id=current_user.id))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('public.v_user_report_new', user_id=current_user.id))
        else:
            report_api = ReportApi()
            report_template = report_api.read(new_user_report.report_id)
            first_section = report_template.ordered_sections[0]
            flash(_('Report created'))
            return redirect(url_for('public.v_user_report_section', report_id=new_user_report.id, user_id=current_user.id,
                                    section_id=first_section.id))
    else:
        return render_template('public/create.html', form=form, title=_('New report'))


@public.route('/user/<int:user_id>/report/<int:user_report_id>', methods=['GET', 'POST'])
@login_required
def v_user_report_edit(user_id, user_report_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
    form = UserReportCreateForm()
    report_api = ReportApi()
    form.report.choices = [(r.id, r.title) for r in report_api.list()]
    try:
        existing_user_report = user_report_api.read(user_report_id)
    except DatabaseItemDoesNotExist as e:
        flash(_('This report does not exist.'))
        return redirect(url_for('public.v_user_report_list_by_user', user_id=current_user.id))
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        return redirect(url_for('public.v_user_report_list_by_user', user_id=current_user.id))
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
                    flash(_('An unexpected error occurred.'))
                    return redirect(url_for('public.v_user_report_list_by_user', user_id=current_user.id))
        try:
            edited_user_report = user_report_api.update(existing_user_report.id, input_data)
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
            return redirect(url_for('public.v_user_report_edit', user_id=current_user.id, report_id=user_report_id))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('public.v_user_report_list_by_user', user_id=current_user.id))
        else:
            return redirect(url_for('public.v_user_report_section', user_id=current_user.id, user_report_id=edited_user_report.id,
                                    section_id=edited_user_report.template.ordered_sections[0].id))
    else:
        form.report.default = str(existing_user_report.report_id)
        form.name.default = existing_user_report.name
        form.process()
        return render_template('public/edit.html', form=form, title=_('Edit report'), report_id=user_report_id)


@public.route('/user/<int:user_id>/report/<int:user_report_id>/section/<int:section_id>', methods=['GET'])
@login_required
def v_user_report_section(user_id, user_report_id, section_id):
    section_api = SectionApi()
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
        return
    try:
        user_report = user_report_api.read(user_report_id)
    except DatabaseItemDoesNotExist as e:
        abort(404)
        return
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        return redirect(url_for('v_index'))

    # Check whether current section is in this user_report
    if section_id not in [section.id for section in user_report.template.sections]:
        abort(404)
        return

    current_section = section_api.read(section_id)

    # Get all question_answers for this report and order them by question_id, so we can compare
    # question.answer.answer_id to question_answers['question_id'].answer_id
    question_answers = {}
    for question_answer in user_report.question_answers:
        question_answers[question_answer.question_id] = question_answer

    return render_template('public/section.html',
                           title=current_section.title,
                           section=current_section,
                           user_report_id=user_report_id,
                           question_answers=question_answers,
                           next_section=current_section.next_in_report,
                           previous_section=current_section.previous_in_report
                           )


@public.route('/user/<int:user_id>/report/<int:user_report_id>/check', methods=['GET'])
@login_required
def v_user_report_check(user_id, user_report_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
    user_report = user_report_api.read(user_report_id)

    # Get all question_answers for this report and order them by question_id, so we can compare
    # question.answer.answer_id to question_answers['question_id'].answer_id
    question_answers = {}
    all_scores = {}

    for section in user_report.template.sections:
        all_scores[section.id] = 0

    for question_answer in user_report.question_answers:
        question_answers[question_answer.question_id] = question_answer
        all_scores[question_answer.question_template.section.id] += question_answer.score * \
                                                                        question_answer.multiplication_factor

    return render_template('public/report.html',
                           report_template=user_report.template,
                           user_report=user_report,
                           user_report_creation_time='{:%Y-%m-%d %H:%M:%S}'.format(user_report.creation_time),
                           question_answers=question_answers,
                           all_scores=all_scores
                           )


@public.route('/user/<int:user_id>/report/<int:user_report_id>/print', methods=['GET'])
@login_required
def v_user_report_print(user_id, user_report_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
