from flask import request, render_template, url_for, redirect, flash
from flask_login import login_required
from flask_babel import gettext as _
from scoremodel.views.admin import admin
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemDoesNotExist, DatabaseItemAlreadyExists
from scoremodel.modules.forms.risk_factors import RiskFactorCreateForm
from scoremodel.modules.forms.generic import GenericCreateForm, GenericDeleteForm
from scoremodel.modules.user.authentication import must_be_admin

lang_api = LangApi()


@admin.route('/risk_factor/list')
@login_required
@must_be_admin
def v_risk_factor_list():
    a_api = RiskFactorApi()
    l_risk_factors = a_api.list()
    return render_template('admin/generic/list.html', items=l_risk_factors, item_type='risk_factor',
                           name='risk_factor', canonical_name=_('Risk Factor'))


@admin.route('/risk_factor/create', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_risk_factor_create():
    form = RiskFactorCreateForm()
    form.lang.choices = [(l.id, l.lang) for l in lang_api.list()]
    if request.method == 'POST' and form.validate_on_submit():
        a_api = RiskFactorApi()
        input_data = {
            'risk_factor': form.risk_factor.data,
            'value': form.value.data,
            'lang_id': form.lang.data
        }
        try:
            a_api.create(input_data)
        except RequiredAttributeMissing:
            flash(_('Missing required form input.'))
            return redirect(url_for('admin.v_risk_factor_create'))
        except DatabaseItemAlreadyExists:
            flash(_('An risk_factor called {0} already exists.').format(input_data['risk_factor']))
            return redirect(url_for('admin.v_risk_factor_create'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            print(e)
            return redirect(url_for('admin.v_risk_factor_create'))
        else:
            flash(_('risk_factor created successfully.'))
            return redirect(url_for('admin.v_risk_factor_list'))
    else:
        return render_template('admin/risk_factor/create.html', action_url=url_for('admin.v_risk_factor_create'),
                               form=form)


@admin.route('/risk_factor/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_risk_factor_edit(id):
    form = RiskFactorCreateForm()
    form.lang.choices = [(l.id, l.lang) for l in lang_api.list()]
    a_api = RiskFactorApi()
    try:
        existing_risk_factor = a_api.read(risk_factor_id=id)
    except DatabaseItemDoesNotExist:
        flash(_('No risk_factor with id {0} exists.').format(id))
        return redirect(url_for('admin.v_risk_factor_list'))
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        return redirect(url_for('admin.v_risk_factor_list'))
    if request.method == 'POST' and form.validate_on_submit():
        input_data = {
            'risk_factor': form.risk_factor.data,
            'value': form.value.data,
            'lang_id': form.lang.data
        }
        try:
            a_api.update(risk_factor_id=id, input_data=input_data)
        except DatabaseItemDoesNotExist:
            flash(_('No risk_factor with id {0}.').format(id))
            return redirect(url_for('admin.v_risk_factor_list'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('admin.v_risk_factor_list'))
        else:
            flash(_('Update successful.'))
            return redirect(url_for('admin.v_risk_factor_list'))
    else:
        # Fill in the values
        form.risk_factor.data = existing_risk_factor.risk_factor
        form.value.data = existing_risk_factor.value
        form.lang.data = existing_risk_factor.lang_id
        return render_template('admin/risk_factor/create.html', form=form,
                               action_url=url_for('admin.v_risk_factor_edit',
                                                  id=id))


@admin.route('/risk_factor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_risk_factor_delete(id):
    form = GenericDeleteForm()
    a_api = RiskFactorApi()
    try:
        existing_risk_factor = a_api.read(id)
    except DatabaseItemDoesNotExist:
        flash(_('This risk factor does not exist.'))
        return redirect(url_for('admin.v_risk_factor_list'))
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        print(e)  # TODO: logging
        return redirect(url_for('admin.v_risk_factor_list'))
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if a_api.delete(id) is True:
                flash(_('Risk factor removed.'))
                return redirect(url_for('admin.v_risk_factor_list'))
            else:
                flash(_('Risk factor could not be removed.'))
                return redirect(url_for('admin.v_risk_factor_list'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            print(e)
            return redirect(url_for('admin.v_risk_factor_list'))
    else:
        return render_template('admin/generic/delete.html', action_url=url_for('admin.v_risk_factor_delete', id=id),
                               item_type=str(existing_risk_factor), item_identifier=existing_risk_factor.risk_factor,
                               form=form)
