from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from scoremodel.modules.user.authentication import LoginForm
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.views.admin import admin
from flask.ext.babel import gettext as _


@admin.route('/login', methods=['GET', 'POST'])
def v_login():
    form = LoginForm()
    a_user = UserApi()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = a_user.get_by_user(form.email.data)
        except DatabaseItemDoesNotExist:
            # User does not exist
            flash(_('Invalid username or password.'))
        else:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('site.v_index'))
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
