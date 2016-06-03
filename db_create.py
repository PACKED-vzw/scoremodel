from scoremodel import db
from scoremodel.models.general import RiskFactor, Report, Answer, Question, Section
from scoremodel.models.public import UserReport, QuestionAnswer
from scoremodel.models.user import Role, User
from scoremodel.models.pages import Page, Document, Lang, MenuLink

##
# TODO: Update for MySQL
##

db.create_all()

