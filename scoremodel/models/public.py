from scoremodel import db
import datetime


class UserReport(db.Model):
    __tablename__ = 'UserReport'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    creation_time = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    report_id = db.Column(db.Integer, db.ForeignKey('Report.id'))
    question_answers = db.relationship('QuestionAnswer', backref='user_report', lazy='dynamic',
                                       cascade='all, delete-orphan')

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

    @property
    def by_section(self):
        questions_by_section = {s.id: {'title': s.title, 'benchmark_count': s.benchmark_count, 'total_weight': s.total_weight, 'questions': []} for s in self.template.sections}
        for question in self.question_answers:
            if question.question_template.section_id in questions_by_section:
                questions_by_section[question.question_template.section_id]['questions'].append(question)
            else:
                questions_by_section[question.question_template.section_id]['questions'] = [question]
        return questions_by_section

    def output_obj(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'report_id': self.report_id,
            'total_score': self.total_score,
            'question_answers': [q.output_obj() for q in self.question_answers],
            'question_answers_by_section': [
                {
                    'section_id': key,
                    'section_title': value['title'],
                    'benchmark_count': value['benchmark_count'],
                    'total_weight': value['total_weight'],
                    'question_answers': [q.output_obj() for q in value['questions']]
                }
                for (key, value) in self.by_section.items()
            ]
        }

    @property
    def total_score(self):
        total_score = 0
        for qa in self.question_answers:
            total_score += qa.score * qa.question_template.section.weight
        return total_score


class QuestionAnswer(db.Model):
    __tablename__ = 'QuestionAnswer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('Answer.id'))
    user_report_id = db.Column(db.Integer, db.ForeignKey(UserReport.id))
    benchmark = db.relationship('Benchmark', primaryjoin="foreign(QuestionAnswer.question_id)==Benchmark.question_id")

    def __init__(self, user_id, question_id, answer_id, user_report_id):
        self.user_id = user_id
        self.question_id = question_id
        self.answer_id = answer_id
        self.user_report_id = user_report_id

    @property
    def score(self):
        return self.question_template.weight * self.answer_template.value * self.question_template.risk_factor.value

    @property
    def weight(self):
        if self.answer_template.value > 0:
            return self.question_template.weight
        return 0

    def output_obj(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'answer_id': self.answer_id,
            'score': self.score,
            'weight': self.weight,
            'user_report_id': self.user_report_id,
            'not_in_benchmark': self.benchmark.not_in_benchmark
        }
