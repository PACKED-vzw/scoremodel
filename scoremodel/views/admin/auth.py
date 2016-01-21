from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from scoremodel.modules.user.authentication import LoginForm
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel import app


@app.route('/admin/login', methods=['GET', 'POST'])
def v_login():
    form = LoginForm()
    a_user = UserApi()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = a_user.get_by_user(form.email.data)
        except DatabaseItemDoesNotExist:
            # User does not exist
            flash('Invalid username or password.')
        else:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('.v_index'))
            else:
                flash('Invalid username or password.')
    ##
    # next=request.args.get('next') must be embedded in the <form action='admin/login?next=next'>, or
    # otherwise the POST request (when you submit the form) will not include the "next" bit.
    return render_template('admin/login.html', form=form, next=request.args.get('next'))


@app.route('/admin/logout', methods=['GET'])
@login_required
def v_logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.v_index'))
