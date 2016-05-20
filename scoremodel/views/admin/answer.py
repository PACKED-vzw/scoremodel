from scoremodel import app
from flask.ext.babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from flask import request, make_response, render_template, redirect, url_for, flash
from flask.ext.login import login_required
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.api.answer import AnswerApi
from scoremodel.modules.forms.generic import GenericDeleteForm
from scoremodel.modules.forms.answers import AnswerCreateForm
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist


@app.route('/admin/answer/list')
@login_required
@must_be_admin
def v_answer_list():
    a_api = AnswerApi()
    l_answers = a_api.list()
    return render_template('admin/generic/list.html', items=l_answers, item_type='answer', name='answer',
                           canonical_name=_('Answer'))


@app.route('/admin/answer/create', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_answer_create():
    form = AnswerCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        a_api = AnswerApi()
        input_data = {
            'answer': form.answer.data,
            'value': form.value.data
        }
        try:
            a_api.create(input_data)
        except RequiredAttributeMissing:
            flash(_('Missing required form input.'))
            return redirect(url_for('.v_answer_create'))
        except DatabaseItemAlreadyExists:
            flash(_('An answer called {0} already exists.').format(input_data['answer']))
            return redirect(url_for('.v_answer_create'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            print(e)
            return redirect(url_for('.v_answer_create'))
        else:
            flash(_('Answer created successfully.'))
            return redirect(url_for('.v_answer_list'))
    return render_template('admin/answer/create.html', action_url=url_for('.v_answer_create'), form=form)


@app.route('/admin/answer/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_answer_edit(id):
    form = AnswerCreateForm()
    a_api = AnswerApi()
    try:
        existing_answer = a_api.read(id)
    except DatabaseItemDoesNotExist:
        flash(_('No answer with id {0} exists.').format(id))
        return redirect(url_for('.v_answer_list'))
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        print(e)
        return redirect(url_for('.v_answer_list'))
    if request.method == 'POST' and form.validate_on_submit():
        input_data = {
            'answer': form.answer.data,
            'value': form.value.data
        }
        try:
            a_api.update(id, input_data=input_data)
        except DatabaseItemDoesNotExist:
            flash('_(No answer with id {0}.').format(id)
            return redirect(url_for('.v_answer_list'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('.v_answer_list'))
        else:
            flash(_('Update successful.'))
            return redirect(url_for('.v_answer_list'))
    # Fill in the values
    form.answer.data = existing_answer.answer
    form.value.data = existing_answer.value
    return render_template('admin/answer/create.html', form=form, action_url=url_for('.v_answer_edit', id=id))


@app.route('/admin/answer/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_answer_delete(id):
    form = GenericDeleteForm()
    a_api = AnswerApi()
    try:
        existing_answer = a_api.read(id)
    except DatabaseItemDoesNotExist:
        flash(_('This answer does not exist.'))
        return redirect(url_for('.v_answer_list'))
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        return redirect(url_for('.v_answer_list'))
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if a_api.delete(id) is True:
                flash(_('Answer removed.'))
                return redirect(url_for('.v_answer_list'))
            else:
                flash(_('Answer could not be removed.'))
                return redirect(url_for('.v_answer_list'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('.v_answer_list'))
    return render_template('admin/generic/delete.html', action_url=url_for('.v_answer_delete', id=id),
                           item_type=str(existing_answer), item_identifier=existing_answer.answer, form=form)
