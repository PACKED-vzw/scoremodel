from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from scoremodel.modules.logger import ScoremodelLogger
from scoremodel.modules.user.authentication import LoginForm
from scoremodel.modules.forms.auth import RegistrationForm, ChangePasswordForm
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.role import RoleApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.organisation_type import OrganisationTypeApi
from scoremodel.modules.api.organisation import OrganisationApi
from scoremodel.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing,\
    InvalidPassword
from scoremodel.views.admin import admin
from flask_babel import gettext as _

a_roles = RoleApi()
logger = ScoremodelLogger()


@admin.route('/login', methods=['GET', 'POST'])
def v_login():
    form = LoginForm()
    a_user = UserApi()
    if request.method == 'POST' and form.validate_on_submit():
        print(form)
        try:
            user = a_user.get_by_user(form.email.data)
        except DatabaseItemDoesNotExist:
            # User does not exist
            flash(_('Invalid username or password.'))
        else:
            if user.verify_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_url = request.args.get('next')
                return redirect(next_url or url_for('site.v_index'))
            else:
                flash(_('Invalid username or password.'))
    ##
    # next=request.args.get('next') must be embedded in the <form action='admin/login?next=next'>, or
    # otherwise the POST request (when you submit the form) will not include the "next" bit.
    return render_template('admin/login.html', form=form, next=request.args.get('next'))


@admin.route('/logout', methods=['GET'])
@login_required
def v_logout():
    logout_user()
    flash(_('You have been logged out.'))
    return redirect(url_for('site.v_index'))


@admin.route('/register', methods=['GET', 'POST'])
def v_register():
    if current_user.is_authenticated:
        # Force logout
        logout_user()
    form = RegistrationForm()
    a_user = UserApi()
    a_role = RoleApi()
    a_lang = LangApi()
    a_o_type = OrganisationTypeApi()
    a_org = OrganisationApi()
    form.language.choices = [(l.id, l.lang) for l in a_lang.list()]
    form.organisation_type.choices = [(t.id, t.type) for t in a_o_type.list()]
    if request.method == 'POST' and form.validate_on_submit():
        user_data = {
            'email': form.email.data,
            'password': form.password.data,
            'username': form.email.data,
            'lang_id': form.language.data
        }
        try:
            public_role = a_role.get_by_role('public')
        except DatabaseItemDoesNotExist:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('admin.v_register'))

        user_data['roles'] = [public_role.id]
        if form.organisation_name:
            # Add to organisation & create
            organisation_data = {
                'name': form.organisation_name.data,
                'size': form.organisation_size.data,
                'type_id': form.organisation_type.data
            }
            try:
                new_organisation = a_org.create(organisation_data)
            except Exception as e:
                flash(_('An unexpected error occurred.'))
                logger.exception(str(e))
                return redirect(url_for('admin.v_register'))
            user_data['organisation_id'] = new_organisation.id
        try:
            new_user = a_user.create(user_data)
        except DatabaseItemAlreadyExists:
            flash(_('This e-mail address is already in use.'))
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
        except Exception as e:  # Remove this after debugging
            #    flash('An unexpected error occurred: {0}'.format(e))
            flash(_('An unexpected error occurred.'))
            logger.exception(str(e))
            return redirect(url_for('admin.v_register'))
        else:
            flash(_('You have been successfully registered. Please log in using your username and password.'))
            return redirect(url_for('admin.v_login'))
    return render_template('admin/user/register.html', form=form)


@admin.route('/change-password', methods=['GET', 'POST'])
@login_required
def v_update_password():
    a_user = UserApi()
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            a_user.check_password(current_user.id, form.old_password.data)
        except InvalidPassword:
            flash(_('Invalid password.'))
            return render_template('admin/user/change_password.html', form=form)
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            logger.exception(str(e))
            return redirect(url_for('admin.v_update_password'))
        try:
            a_user.update_password(current_user.id, form.new_password.data)
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            logger.exception(str(e))
            return redirect(url_for('admin.v_update_password'))
        else:
            flash(_('Your password has been successfully changed.'))
            return redirect(url_for('site.v_index'))

    return render_template('admin/user/change_password.html', form=form)


@admin.route('/forgotten-password', methods=['GET', 'POST'])
def v_forgotten_password():
    pass
