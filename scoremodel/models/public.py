from scoremodel import db
from scoremodel.models.general import Question, Answer, Report
from scoremodel.models.user import User


class UserReport(db.Model):
    __tablename__ = 'UserReport'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    report_date = db.Column(db.Date)
    report_id = db.Column(db.Integer, db.ForeignKey(Report.id))
    questions = db.relationship('QuestionAnswer', backref='report', lazy='dynamic')


class QuestionAnswer(db.Model):
    __tablename__ = 'QuestionAnswer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    answer_id = db.Column(db.Integer, db.ForeignKey(Answer.id))
    user_report_id = db.Column(db.Integer, db.ForeignKey(UserReport.id))
    # question_id
    # user_id
    # answer_id
    # user_report_id


    # user_id
    # report_name
    # report_id
