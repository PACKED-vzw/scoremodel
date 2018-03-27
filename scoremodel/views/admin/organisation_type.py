from flask import request, render_template, url_for, redirect, flash
from flask_login import login_required
from flask_babel import gettext as _
from scoremodel.views.admin import admin
from scoremodel.modules.api.organisation_type import OrganisationTypeApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemDoesNotExist, DatabaseItemAlreadyExists
from scoremodel.modules.forms.organisation_type import OrganisationTypeCreateForm
from scoremodel.modules.forms.generic import GenericCreateForm, GenericDeleteForm
from scoremodel.modules.user.authentication import must_be_admin


@admin.route('/organisation_type/list')
@login_required
@must_be_admin
def v_organisation_type_list():
    l_organisation_types = OrganisationTypeApi().list()
    return render_template('admin/generic/list.html', items=l_organisation_types, item_type='organisation_type',
                           name='type', canonical_name=_('Organisation type'))


@admin.route('/organisation_type/create', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_organisation_type_create():
    form = OrganisationTypeCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        a_api = OrganisationTypeApi()
        input_data = {
            'type': form.name.data
        }
        try:
            a_api.create(input_data)
        except RequiredAttributeMissing:
            flash(_('Missing required form input.'))
            return redirect(url_for('admin.v_organisation_type_create'))
        except DatabaseItemAlreadyExists:
            flash(_('An organisation_type called {0} already exists.').format(input_data['type']))
            return redirect(url_for('admin.v_organisation_type_create'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            print(e)
            return redirect(url_for('admin.v_organisation_type_create'))
        else:
            flash(_('organisation_type created successfully.'))
            return redirect(url_for('admin.v_organisation_type_list'))
    else:
        return render_template('admin/generic/create.html', action_url=url_for('admin.v_organisation_type_create'),
                               form=form, canonical_name=_('Organisation type'))


@admin.route('/organisation_type/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_organisation_type_edit(id):
    form = OrganisationTypeCreateForm()
    a_api = OrganisationTypeApi()
    try:
        existing_org_type = a_api.read(id)
    except DatabaseItemDoesNotExist:
        flash(_('No organisation_type with id {0} exists.').format(id))
        return redirect(url_for('admin.v_organisation_type_list'))
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        return redirect(url_for('admin.v_organisation_type_list'))
    if request.method == 'POST' and form.validate_on_submit():
        input_data = {
            'type': form.name.data
        }
        try:
            a_api.update(id, input_data)
        except DatabaseItemDoesNotExist:
            flash(_('No organisation_type with id {0}.').format(id))
            return redirect(url_for('admin.v_organisation_type_list'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('admin.v_organisation_type_list'))
        else:
            flash(_('Update successful.'))
            return redirect(url_for('admin.v_organisation_type_list'))
    else:
        # Fill in the values
        form.name.data = existing_org_type.type
        return render_template('admin/generic/create.html', form=form,
                               action_url=url_for('admin.v_organisation_type_edit', id=id),
                               canonical_name=_('Organisation type'))


@admin.route('/organisation_type/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_organisation_type_delete(id):
    form = GenericDeleteForm()
    a_api = OrganisationTypeApi()
    try:
        existing_org_type = a_api.read(id)
    except DatabaseItemDoesNotExist:
        flash(_('This organisation_type does not exist.'))
        return redirect(url_for('admin.v_organisation_type_list'))
    except Exception as e:
        flash(_('An unexpected error occurred.'))
        return redirect(url_for('admin.v_organisation_type_list'))
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if a_api.delete(id) is True:
                flash(_('Organisation type removed.'))
                return redirect(url_for('admin.v_organisation_type_list'))
            else:
                flash(_('Organisation type could not be removed.'))
                return redirect(url_for('admin.v_organisation_type_list'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('admin.v_organisation_type_list'))
    else:
        return render_template('admin/generic/delete.html', action_url=url_for('admin.v_organisation_type_delete',
                                                                               id=id),
                               item_type=str(existing_org_type), item_identifier=existing_org_type.type,
                               form=form)
