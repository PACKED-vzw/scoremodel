from sqlalchemy import and_
from scoremodel import db
from scoremodel.models.public import QuestionAnswer

##
# Contains general database models:
#   Rapport
#   Sectie
#   Vraag
#
# These models contain the questions etc., not the user replies. See users.py
##
"""
•	Vraag
o	Context
o	Risico
o	Voorbeeld
o	Acties
o	Risicofactor
o	Wegingsfactor
•	Sectie
o	Rel bevat Vragen
o	Titel
o	Context
o	Aggregatiescore totaal
•	Rapport
    Benchmark
Acties
Risicofactor
"""


class Answer(db.Model):
    __tablename__ = 'Answer'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(255), nullable=False, index=True)
    value = db.Column(db.Integer, nullable=True, default=1)
    order_in_question = db.Column(db.Integer, nullable=False, default=0)
    lang_id = db.Column(db.Integer, db.ForeignKey('Lang.id'))
    question_answers = db.relationship('QuestionAnswer', backref='answer_template', lazy='dynamic')
    benchmark = db.relationship('Benchmark', backref='answer', lazy='dynamic')

    def __repr__(self):
        return u'<Answer {0}: {1}>'.format(self.id, self.answer)

    def __init__(self, answer, lang_id, value=1, order=0):
        self.answer = answer
        self.lang_id = lang_id
        self.value = value
        self.order_in_question = order

    def output_obj(self):
        return {
            'id': self.id,
            'answer': self.answer,
            'value': self.value,
            'lang_id': self.lang_id,
            'order_in_question': self.order_in_question
        }


answers = db.Table('answer_question',
                   db.Column('answer_id', db.Integer, db.ForeignKey('Answer.id')),
                   db.Column('question_id', db.Integer, db.ForeignKey('Question.id'))
                   )


class RiskFactor(db.Model):
    __tablename__ = 'RiskFactor'
    id = db.Column(db.Integer, primary_key=True)
    risk_factor = db.Column(db.String(190), index=True, unique=True)
    value = db.Column(db.Integer, nullable=False, default=1)
    lang_id = db.Column(db.Integer, db.ForeignKey('Lang.id'))
    questions_single = db.relationship('Question', backref='risk_factor', lazy='dynamic')

    def __repr__(self):
        return '<RiskFactor {0}>'.format(self.id)

    def __init__(self, risk_factor, lang_id, value=None):
        self.risk_factor = risk_factor
        self.lang_id = lang_id
        if value:
            self.value = value

    def output_obj(self):
        return {
            'id': self.id,
            'risk_factor': self.risk_factor,
            'lang_id': self.lang_id,
            'value': self.value
        }


risk_factors = db.Table('riskfactor_question',
                        db.Column('risk_factor_id', db.Integer, db.ForeignKey('RiskFactor.id')),
                        db.Column('question_id', db.Integer, db.ForeignKey('Question.id'))
                        )


class Report(db.Model):
    __tablename__ = 'Report'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    sections = db.relationship('Section', backref='report', lazy='dynamic', cascade='all, delete-orphan')
    lang_id = db.Column(db.Integer, db.ForeignKey('Lang.id'))
    user_reports = db.relationship('UserReport', backref='template', lazy='dynamic', cascade='all, delete-orphan')
    benchmark_reports = db.relationship('BenchmarkReport', backref='report', lazy='dynamic',
                                        cascade='all, delete-orphan')

    def __repr__(self):
        return '<Report {0}>'.format(self.id)

    def __init__(self, title, lang_id):
        self.title = title
        self.lang_id = lang_id

    def output_obj(self):
        return {
            'id': self.id,
            'title': self.title,
            'lang_id': self.lang_id,
            'sections': [s.output_obj() for s in self.ordered_sections],
            'benchmark_reports': [b.id for b in self.benchmark_reports]
        }

    @property
    def ordered_sections(self):
        return sorted(self.sections, key=lambda section: section.order_in_report)


class Section(db.Model):
    __tablename__ = 'Section'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    context = db.Column(db.Text)
    order_in_report = db.Column(db.Integer, nullable=False, default=0)
    weight = db.Column(db.Integer, nullable=False, default=1)
    questions = db.relationship('Question', backref='section', lazy='dynamic', cascade='all, delete-orphan')
    report_id = db.Column(db.Integer, db.ForeignKey(Report.id))
    maximum_score = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return u'<Section {0}: {1}>'.format(self.id, self.title)

    def __init__(self, title, context=None, order=0, weight=1):
        self.title = title
        self.context = context
        self.order_in_report = order
        self.weight = weight

    def output_obj(self):
        if not self.next_in_report:
            next_section_id = None
        else:
            next_section_id = self.next_in_report.id

        if not self.previous_in_report:
            previous_section_id = None
        else:
            previous_section_id = self.previous_in_report.id
        return {
            'id': self.id,
            'title': self.title,
            'context': self.context,
            'order_in_report': self.order_in_report,
            'questions': [q.output_obj() for q in self.ordered_questions],
            'report_id': self.report_id,
            'weight': self.weight,
            'next_section_id': next_section_id,
            'previous_section_id': previous_section_id
        }

    @property
    def highest_order(self):
        return self.ordered_questions[-1].order_in_section

    @property
    def ordered_questions(self):
        return sorted(self.questions, key=lambda question: question.order_in_section)

    @property
    def next_in_report(self):
        current_pos = self.report.ordered_sections.index(self)
        next_pos = current_pos + 1
        if next_pos >= len(self.report.ordered_sections):
            return None
        else:
            return self.report.ordered_sections[next_pos]

    @property
    def previous_in_report(self):
        current_pos = self.report.ordered_sections.index(self)
        previous_pos = current_pos - 1
        if previous_pos < 0:
            return None
        else:
            return self.report.ordered_sections[previous_pos]


class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(512), index=True, nullable=False)
    context = db.Column(db.Text)
    risk = db.Column(db.Text)
    example = db.Column(db.Text)
    weight = db.Column(db.Integer, nullable=False, default=1)
    order_in_section = db.Column(db.Integer, nullable=False, default=0)
    section_id = db.Column(db.Integer, db.ForeignKey(Section.id))
    action = db.Column(db.Text)
    maximum_score = db.Column(db.Integer, nullable=False, default=0)
    risk_factor_id = db.Column(db.Integer, db.ForeignKey(RiskFactor.id))
    risk_factors = db.relationship('RiskFactor',
                                   secondary=risk_factors,
                                   primaryjoin=(risk_factors.c.question_id == id),
                                   secondaryjoin=(risk_factors.c.risk_factor_id == RiskFactor.id),
                                   backref=db.backref('questions', lazy='dynamic'),
                                   lazy='dynamic'
                                   )
    answers = db.relationship('Answer',
                              secondary=answers,
                              primaryjoin=(answers.c.question_id == id),
                              secondaryjoin=(answers.c.answer_id == Answer.id),
                              backref=db.backref('questions', lazy='dynamic'),
                              lazy='dynamic'
                              )
    question_answers = db.relationship('QuestionAnswer', backref='question_template', lazy='dynamic',
                                       cascade='all, delete-orphan')
    benchmark = db.relationship('Benchmark', backref='question', lazy='dynamic', cascade='all, delete-orphan')

    # TODO: make weight dependent on risk_factors! (risk_factors must have a weight: hoog: 3, midden: 2, laag: 1

    def __repr__(self):
        return u'<Question {0}: {1}>'.format(self.id, self.question)

    def __init__(self, question, context=None, risk=None, example=None, weight=1, order=0, action=None):
        self.question = question
        self.context = context
        self.risk = risk
        self.example = example
        self.weight = weight
        self.order_in_section = order
        self.action = action

    def selected_answer(self, user_report_id):
        """
        Returns the selected answer for a specific question in a specific user report
        :param user_report_id:
        :return:
        """
        return QuestionAnswer.query.filter(and_(QuestionAnswer.question_id == self.id,
                                                QuestionAnswer.user_report_id == user_report_id)).first()

    def ordered_risk_factors(self):
        return sorted(self.risk_factors, key=lambda r: r.value, reverse=True)

    @property
    def ordered_answers(self):
        return sorted(self.answers, key=lambda a: a.value, reverse=True)

    def output_obj(self):
        return {
            'id': self.id,
            'question': self.question,
            'context': self.context,
            'risk': self.risk,
            'example': self.example,
            'weight': self.weight,
            'order_in_section': self.order_in_section,
            'section_id': self.section_id,
            'action': self.action,
            'risk_factor_id': self.risk_factor_id,
            'answers': [a.output_obj() for a in self.answers],
            'ordered_answers': [a.output_obj() for a in self.ordered_answers]
        }


class BenchmarkReport(db.Model):
    __tablename__ = 'BenchmarkReport'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    report_id = db.Column(db.Integer, db.ForeignKey(Report.id))
    benchmarks = db.relationship('Benchmark', backref='benchmark_report', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, title):
        self.title = title

    def output_obj(self):
        return {
                'id': self.id,
                'title': self.title,
                'report_id': self.report_id,
                'benchmarks': [b.output_obj() for b in self.benchmarks],
                'benchmarks_by_section': []
            }


class Benchmark(db.Model):
    __tablename__ = 'Benchmark'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    answer_id = db.Column(db.Integer, db.ForeignKey(Answer.id))
    benchmark_report_id = db.Column(db.Integer, db.ForeignKey(BenchmarkReport.id))
    not_in_benchmark = db.Column(db.Boolean, default=False)

    def __init__(self):
        pass

    @property
    def score(self):
        if self.answer is None:
            return 0
        else:
            return self.question.weight * self.answer.value * self.question.risk_factor.value

    def output_obj(self):
        # The last case shouldn't happen: TODO: fix
        if self.not_in_benchmark or self.answer is None or self.question.risk_factor is None:
            return {
                'id': self.id,
                'question_id': self.question_id,
                'benchmark_report_id': self.benchmark_report_id,
                'not_in_benchmark': self.not_in_benchmark
            }
        else:
            return {
                'id': self.id,
                'question_id': self.question_id,
                'answer_id': self.answer_id,
                'score': self.score,
                'benchmark_report_id': self.benchmark_report_id,
                'not_in_benchmark': self.not_in_benchmark
            }
