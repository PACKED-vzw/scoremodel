from scoremodel import db


class QuestionAnswer(db.Model):
    __tablename__ = 'question_answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # question_id
    # user_id
    # answer_id
    # user_report_id


class UserReport(db.Model):
    __tablename__ = 'user_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # user_id
    # report_name
    # report_id
