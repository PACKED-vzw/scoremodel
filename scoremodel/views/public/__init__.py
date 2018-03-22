from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from flask_login import login_required, current_user
from flask_babel import gettext as _

from scoremodel.modules.report.color import Color
from scoremodel.modules.api.question_answer import QuestionAnswerApi
from scoremodel.modules.api.report import ReportApi
from scoremodel.modules.api.section import SectionApi
from scoremodel.modules.api.question import QuestionApi
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.user_report import UserReportApi
from scoremodel.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing
from scoremodel.modules.forms.public.report import UserReportCreateForm
from scoremodel.modules.forms.generic import GenericDeleteForm
from scoremodel.modules.locale import Locale

public = Blueprint('public', __name__, url_prefix='/scoremodel')

user_report_api = UserReportApi()
locale_api = Locale()


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


@public.route('/user/<int:user_id>/report/<int:user_report_id>/delete', methods=['GET', 'POST'])
@login_required
def v_user_report_delete(user_id, user_report_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
    form = GenericDeleteForm()
    try:
        existing_report = user_report_api.read(user_report_id)
    except DatabaseItemDoesNotExist:
        flash(_('No report with id {0} exists.').format(user_report_id))
        return url_for('public.v_user_report_list_by_user', user_id=user_id)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if user_report_api.delete(user_report_id) is True:
                flash(_('Report {0} removed.').format(existing_report.name))
            else:
                flash(_('Failed to remove report {0}.').format(existing_report.name))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return render_template('public/generic/delete.html', action_url=url_for('public.v_user_report_delete',
                                                                                    user_report_id=user_report_id,
                                                                                    user_id=user_id),
                                   item_type=_('Report'), item_identifier=existing_report.name, form=form)
        else:
            return redirect(url_for('public.v_user_report_list_by_user', user_id=user_id))
    return render_template('public/generic/delete.html', action_url=url_for('public.v_user_report_delete',
                                                                            user_report_id=user_report_id,
                                                                            user_id=user_id),
                           item_type=_('Report'), item_identifier=existing_report.name, form=form)


@public.route('/user/<int:user_id>/report/new', methods=['GET', 'POST'])
@login_required
def v_user_report_new(user_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
    form = UserReportCreateForm()
    report_api = ReportApi()
    choices = [(r.id, r.title) for r in report_api.by_lang(locale_api.current_locale)]
    if len(choices) == 0:
        choices = [(r.id, r.title) for r in report_api.by_lang(locale_api.fallback_locale)]
    form.report.choices = choices
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
            return redirect(
                url_for('public.v_user_report_section', user_report_id=new_user_report.id, user_id=current_user.id,
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
        if input_data['report_id'] != existing_user_report.report_id:
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
            return redirect(
                url_for('public.v_user_report_section', user_id=current_user.id, user_report_id=edited_user_report.id,
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
        return redirect(url_for('site.v_index'))

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

    benchmarks_by_section = user_report_api.benchmarks_by_section(user_report_id)

    # Create a color-range for the risk_factors
    risk_factors = [r.risk_factor for r in RiskFactorApi().list()]
    colored_risk_factors = Color().range(risk_factors)

    return render_template('public/section.html',
                           title=current_section.title,
                           section=current_section,
                           user_report_id=user_report_id,
                           question_answers=question_answers,
                           next_section=current_section.next_in_report,
                           previous_section=current_section.previous_in_report,
                           benchmarks_by_section=benchmarks_by_section,
                           colored_risk_factors=colored_risk_factors
                           )


@public.route('/user/<int:user_id>/report/<int:user_report_id>/check', methods=['GET'])
@public.route('/user/<int:user_id>/report/<int:user_report_id>/full', methods=['GET'])
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
    highest_answers = {}

    for section in user_report.template.sections:
        all_scores[section.id] = 0

    for question_answer in user_report.question_answers:
        question = question_answer.question_template
        question_answers[question.id] = question_answer
        multiplication_factor = SectionApi().multiplication_factor(question.section_id)
        all_scores[question.section_id] += question_answer.score * multiplication_factor
        sorted_answers = sorted(question.answers, key=lambda a: a.value, reverse=True)
        if len(sorted_answers) > 0:
            highest_answers[question.id] = sorted_answers[0].value
        else:
            highest_answers[question.id] = 0

    benchmarks_by_section = user_report_api.benchmarks_by_section(user_report_id)

    # Create a color-range for the risk_factors
    risk_factors = [r.risk_factor for r in RiskFactorApi().list()]
    colored_risk_factors = Color().range(risk_factors)

    return render_template('public/report.html',
                           report_template=user_report.template,
                           user_report=user_report,
                           user_report_creation_time='{:%Y-%m-%d %H:%M:%S}'.format(user_report.creation_time),
                           question_answers=question_answers,
                           all_scores=all_scores,
                           benchmarks_by_section=benchmarks_by_section,
                           highest_answers=highest_answers,
                           colored_risk_factors=colored_risk_factors
                           )


@public.route('/user/<int:user_id>/report/<int:user_report_id>/summary', methods=['GET'])
@login_required
def v_user_report_summary(user_id, user_report_id):
    if current_user.id != user_id:
        flash(_('You can only view your own reports.'))
        abort(403)
    user_report = user_report_api.read(user_report_id)

    question_answers = {}
    all_scores = {}

    for section in user_report.template.sections:
        all_scores[section.id] = 0

    for question_answer in user_report.question_answers:
        question_answers[question_answer.question_id] = question_answer
        multiplication_factor = SectionApi().multiplication_factor(question_answer.question_template.section_id)
        all_scores[question_answer.question_template.section.id] += question_answer.score * \
                                                                    multiplication_factor

    highest_unanswered = []

    for question in ReportApi().questions_by_combined_weight(user_report.template.id):
        if question['question_id'] not in question_answers or question_answers[question['question_id']].score < \
                question['max_score']:
            try:
                highest_unanswered.append(QuestionApi().read(question['question_id']))
            except DatabaseItemDoesNotExist:
                pass

    if len(highest_unanswered) >= 5:
        visible_unanswered = highest_unanswered[:5]
    else:
        visible_unanswered = highest_unanswered

    benchmarks_by_question = {}
    for bm_r in user_report.template.benchmark_reports:
        for bm in bm_r.benchmarks:
            if bm.question_id in benchmarks_by_question:
                benchmarks_by_question[bm.question_id].append(bm)
            else:
                benchmarks_by_question[bm.question_id] = [bm]

    # Create a color-range for the risk_factors
    risk_factors = [r.risk_factor for r in RiskFactorApi().list()]
    colored_risk_factors = Color().range(risk_factors)

    return render_template('public/summary.html',
                           report_template=user_report.template,
                           user_report=user_report,
                           user_report_creation_time='{:%Y-%m-%d %H:%M:%S}'.format(user_report.creation_time),
                           highest_unanswered=visible_unanswered,
                           benchmarks_by_question=benchmarks_by_question,
                           question_answers_by_id=question_answers,
                           colored_risk_factors=colored_risk_factors
                           )
