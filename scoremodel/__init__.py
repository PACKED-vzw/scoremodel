from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
babel = Babel(app)
# Models must be imported after db has been declared
from scoremodel.views.user import *
from scoremodel.views.api import *
import scoremodel.views.admin
from scoremodel.models import *


@app.route('/')
@app.route('/index')
@app.route('/home')
def v_index():
    return 'Hello World!'


@app.route('/scoremodel')
def v_scoremodel():
    return ''


@app.route('/faq')
def v_faq():
    pass


@app.route('/documenten')
def v_documenten():
    pass


@app.route('/disclaimer')
def v_disclaimer():
    pass


@app.route('/admin')
def v_admin():
    pass


if __name__ == '__main__':
    app.run()
