from flask import Flask, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from flask.ext.login import LoginManager, current_user
from flask.ext.markdown import Markdown
from scoremodel.modules.setup import AppSetup

app = AppSetup().app
db = SQLAlchemy(app)
Markdown(app)
babel = Babel(app)
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

# TODO: probleem met vragen van rapporten


@babel.localeselector
def get_locale():
    if current_user.is_anonymous or not current_user.locale:
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    else:
        return current_user.locale


@app.route('/')
def v_index():
    return redirect(url_for('site.v_index'))

if __name__ == '__main__':
    app.run()
