from scoremodel.modules.setup import AppSetup
from flask.ext.sqlalchemy import SQLAlchemy
from scoremodel.models.general import RiskFactor, Report, Answer, Question, Section
from scoremodel.models.public import UserReport, QuestionAnswer
from scoremodel.models.user import Role, User
from scoremodel.models.pages import Page, Document, Lang, MenuLink

##
# TODO: Update for MySQL
##

app = AppSetup().app
db = SQLAlchemy(app)

db.create_all()

