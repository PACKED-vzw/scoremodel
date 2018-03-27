from flask import render_template, url_for, flash, request, redirect
from flask_login import login_required, current_user
from flask_babel import gettext as _
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.role import RoleApi
from scoremodel.modules.user.admin import UserCreateForm, UserDeleteForm, UserModifyForm
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist
from scoremodel.views.admin import admin

from scoremodel import app

a_roles = RoleApi()


@admin.route('/user/view/<int:user_id>')
@login_required
@must_be_admin
def v_user_view(user_id):
    pass


@admin.route('/user/list', methods=['GET'])
@login_required
@must_be_admin
def v_user_list():
    a_user = UserApi()
    l_users = a_user.list()
    return render_template('admin/user/list.html', users=l_users)


@admin.route('/user/create', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_user_create():
    db_roles = a_roles.list()
    possible_roles = []
    for db_role in db_roles:
        possible_roles.append((db_role.id, db_role.role))
    form = UserCreateForm()
    form.roles.choices = possible_roles

    if request.method == 'POST' and form.validate_on_submit():
        a_user = UserApi()
        input_data = {
            'email': form.email.data,
            'password': form.password.data,
            'roles': form.roles.data,
            'username': form.email.data,

        }
        try:
            new_user = a_user.create(input_data)
        except DatabaseItemAlreadyExists as e:
            flash(_('A user called {0} already exists.').format(input_data['email']))
            return render_template('admin/user/create.html', form=form)
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
            return render_template('admin/user/create.html', form=form)
        except Exception as e:  # Remove this after debugging
            #    flash('An unexpected error occurred: {0}'.format(e))
            flash(_('An unexpected error occurred.'))
            return render_template('admin/user/create.html', form=form)
        else:
            return redirect(url_for('admin.v_user_list'))

    return render_template('admin/user/create.html', form=form)


@admin.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_user_edit(user_id):
    form = UserModifyForm()
    a_user = UserApi()
    db_roles = a_roles.list()
    possible_roles = []
    for db_role in db_roles:
        possible_roles.append((db_role.id, db_role.role))
    form.roles.choices = possible_roles
    try:
        existing_user = a_user.read(user_id)
    except DatabaseItemDoesNotExist:
        flash(_('A user with id {0} does not exist.').format(user_id))
        return redirect(url_for('admin.v_user_list'))

    if request.method == 'POST' and form.validate_on_submit():
        input_data = {
            'email': form.email.data,
            'password': form.password.data,
            'roles': form.roles.data
        }
        ##
        # We very much dislike empty passwords, so we assume that, if the password field
        # is empty, the user didn't want to change it.
        if input_data['password'] == '' or input_data['password'] is None:
            update_password = False
        else:
            update_password = True

        try:
            edited_user = a_user.update(user_id, input_data, update_password)
        except DatabaseItemDoesNotExist as e:
            flash(_('No user with id {0}').format(user_id))
            return redirect(url_for('admin.v_user_list'))
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
            return render_template('admin/user/edit.html', form=form, user_id=user_id)
        except Exception as e:
            flash(_('An unexpected error occurred: {0}').format(e))
            # flash('An unexpected error occurred.')
            return render_template('admin/user/edit.html', form=form, user_id=user_id)
        else:
            return redirect(url_for('admin.v_user_list'))
    else:
        ##
        # Add the data from the existing user for the edit form. This must be done after validate_on_submit()
        # or it will overwrite the data from the submitted form.
        form.email.default = existing_user.email
        roles_default = []
        for role in existing_user.roles:
            roles_default.append(str(role.id))
        form.roles.default = roles_default
        # http://stackoverflow.com/questions/5519729/wtforms-how-to-select-options-in-selectmultiplefield
        form.process()

        return render_template('admin/user/edit.html', form=form, user_id=user_id)


@admin.route('/user/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_user_delete(user_id):
    form = UserDeleteForm()
    a_user = UserApi()
    try:
        existing_user = a_user.read(user_id)
    except DatabaseItemDoesNotExist as e:
        flash(_('No user with id {0}').format(user_id))
        return redirect(url_for('admin.v_user_list'))
    except Exception as e:
        flash(_('An unexpected error occurred: {0}').format(e))
        # flash('An unexpected error occurred.')
        return redirect(url_for('admin.v_user_list'))

    if request.method == 'POST' and form.validate_on_submit():
        if a_user.delete(user_id) is True:
            flash(_('User {0} deleted').format(existing_user.email))
            return redirect(url_for('admin.v_user_list'))
        else:
            flash(_('Unable to delete user {0}').format(existing_user.email))
            return render_template('admin/generic/delete.html', action_url=url_for('admin.v_user_delete',
                                                                                   user_id=user_id),
                                   item_type=_('User'), item_identifier=existing_user.email, form=form)

    return render_template('admin/generic/delete.html', action_url=url_for('admin.v_user_delete', user_id=user_id),
                           item_type=_('User'), item_identifier=existing_user.email, form=form)


# For registered users
@admin.route('/profile', methods=['GET'])
@login_required
def v_user_profile():
    user = {
        'name': current_user.username,
        'language': app.config['BABEL_DEFAULT_LOCALE']
    }
    if current_user.lang is not None:
        user['language'] = current_user.lang.lang
    organisation = {
        'name': '',
        'type': '',
        'size': 0
    }
    if current_user.organisation is not None:
        organisation['name'] = current_user.organisation.name
        organisation['type'] = current_user.organisation.type.type
        organisation['size'] = current_user.organisation.size if not None else 0
    return render_template('admin/user/profile.html', user=user, organisation=organisation)
