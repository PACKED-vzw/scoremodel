from scoremodel import db
import datetime


class UserReport(db.Model):
    __tablename__ = 'UserReport'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    creation_time = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    report_id = db.Column(db.Integer, db.ForeignKey('Report.id'))
    question_answers = db.relationship('QuestionAnswer', backref='user_report', lazy='dynamic')

    def __init__(self, name, user_id, report_id, creation_time=None):
        self.name = name
        self.user_id = user_id
        self.report_id = report_id
        if creation_time is None:
            creation_time = datetime.datetime.now()
        self.creation_time = creation_time
        self.last_modified = creation_time

    @property
    def creation_date(self):
        return self.creation_time.date()

    def output_obj(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'report_id': self.report_id,
            'question_answers': [q.output_obj() for q in self.question_answers]
        }


class QuestionAnswer(db.Model):
    __tablename__ = 'QuestionAnswer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('Answer.id'))
    user_report_id = db.Column(db.Integer, db.ForeignKey(UserReport.id))

    def __init__(self, user_id, question_id, answer_id, user_report_id):
        self.user_id = user_id
        self.question_id = question_id
        self.answer_id = answer_id
        self.user_report_id = user_report_id

    @property
    def score(self):
        return self.question_template.weight * self.answer_template.value

    @property
    def multiplication_factor(self):
        return self.question_template.section.multiplication_factor

    def output_obj(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'answer_id': self.answer_id,
            'score': self.score,
            'multiplication_factor': self.multiplication_factor,
            'user_report_id': self.user_report_id
        }
