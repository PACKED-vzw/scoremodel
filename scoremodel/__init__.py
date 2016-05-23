from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from scoremodel.modules.setup import AppSetup

app = AppSetup().app
db = SQLAlchemy(app)
babel = Babel(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = 'v_login'


# Models must be imported after db has been declared
from scoremodel.views.api_old import *
from scoremodel.views.admin import *
from scoremodel.views.admin.report import *
from scoremodel.views.admin.auth import *
from scoremodel.views.admin.user import *
from scoremodel.views.admin.answer import *
from scoremodel.views.admin.risk_factor import *

# Blueprints
from scoremodel.views.api import api
app.register_blueprint(api)
from scoremodel.views.public import public
app.register_blueprint(public)

# TODO: probleem met vragen van rapporten


@babel.localeselector
def get_locale():
    if current_user.is_anonymous or not current_user.locale:
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    else:
        return current_user.locale

@app.route('/')
@app.route('/index')
@app.route('/home')
def v_index():
    return 'Hello World!'

@app.route('/faq')
def v_faq():
    pass


@app.route('/documenten')
def v_doc():
    pass


@app.route('/disclaimer')
def v_disclaimer():
    pass


@app.route('/contact')
def v_contact():
    pass

if __name__ == '__main__':
    app.run()
