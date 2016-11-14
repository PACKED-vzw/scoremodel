from flask import Flask, request, redirect, url_for, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel, gettext as _
from flask.ext.login import LoginManager, current_user
from flask.ext.markdown import Markdown
from flask_wtf.csrf import CsrfProtect
from scoremodel.modules.setup import AppSetup

app = AppSetup().app
db = SQLAlchemy(app)
Markdown(app)
babel = Babel(app)
csrf = CsrfProtect(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = 'admin.v_login'


# Blueprints
from scoremodel.views.api import api
app.register_blueprint(api)
from scoremodel.views.public import public
app.register_blueprint(public)
from scoremodel.views.site import site
app.register_blueprint(site)
from scoremodel.views.admin import admin
app.register_blueprint(admin)
from scoremodel.modules.locale import Locale
from scoremodel.modules.setup.first_time import add_admin, add_lang, add_menu_links, add_roles, check_has_admin,\
    check_has_tables, add_tables
from scoremodel.modules.forms.setup import SetupForm
from scoremodel.modules.user.anonymous import ScAnonymousUser


login_manager.anonymous_user = ScAnonymousUser

# TODO: probleem met vragen van rapporten


@babel.localeselector
def get_locale():
    locale_selector = Locale()
    locale_selector.set_session_locale(locale_selector.current_locale)
    return locale_selector.current_locale


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route('/')
def v_index():
    if check_has_tables() is not True or check_has_admin() is not True:
        return redirect(url_for('v_setup'))
    else:
        return redirect(url_for('site.v_index'))


@app.route('/setup', methods=['GET', 'POST'])
def v_setup():
    form = SetupForm()
    if request.method == 'POST' and form.validate_on_submit():
        create_functions = (add_tables, add_roles, add_lang, add_menu_links)
        for func in create_functions:
            try:
                func()
            except Exception as e:
                flash(_('An unexpected error occurred: {0}').format(e))
                db.drop_all()
                return render_template('setup.html', form=form)
        try:
            admin = add_admin()
        except Exception as e:
            flash(_('An unexpected error occurred: {0}').format(e))
            db.drop_all()
            return render_template('setup.html', form=form)
        return render_template('setup.html', username=admin['user'].email, password=admin['password'])
    else:
        return render_template('setup.html', form=form)


@app.errorhandler(400)
def bad_request(e):
    return e


if __name__ == '__main__':
    app.run()
