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
Acties
Risicofactor
"""


class Answer(db.Model):
    __tablename__ = 'Answer'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False, index=True)
    value = db.Column(db.Integer, nullable=True, default=1)
    order_in_question = db.Column(db.Integer, nullable=False, default=0)
    question_answers = db.relationship('QuestionAnswer', backref='answer_template', lazy='dynamic')

    def __repr__(self):
        return u'<Answer {0}: {1}>'.format(self.id, self.answer)

    def __init__(self, answer, value=1, order=0):
        self.answer = answer
        self.value = value
        self.order_in_question = order

    def output_obj(self):
        return {
            'id': self.id,
            'answer': self.answer,
            'value': self.value,
            'order_in_question': self.order_in_question
        }


answers = db.Table('answer_question',
                   db.Column('answer_id', db.Integer, db.ForeignKey('Answer.id')),
                   db.Column('question_id', db.Integer, db.ForeignKey('Question.id'))
                   )


class RiskFactor(db.Model):
    __tablename__ = 'RiskFactor'
    id = db.Column(db.Integer, primary_key=True)
    risk_factor = db.Column(db.Text, index=True, unique=True)
    value = db.Column(db.Integer, nullable=False, default=1)
    questions_single = db.relationship('Question', backref='risk_factor', lazy='dynamic')

    def __repr__(self):
        return '<RiskFactor {0}>'.format(self.id)

    def __init__(self, risk_factor, value=None):
        self.risk_factor = risk_factor
        if value:
            self.value = value

    def output_obj(self):
        return {
            'id': self.id,
            'risk_factor': self.risk_factor,
            'value': self.value
        }


risk_factors = db.Table('riskfactor_question',
                        db.Column('risk_factor_id', db.Integer, db.ForeignKey('RiskFactor.id')),
                        db.Column('question_id', db.Integer, db.ForeignKey('Question.id'))
                        )


class Report(db.Model):
    __tablename__ = 'Report'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, index=True, nullable=False)
    sections = db.relationship('Section', backref='report', lazy='dynamic')
    user_reports = db.relationship('UserReport', backref='template', lazy='dynamic')

    def __repr__(self):
        return '<Report {0}>'.format(self.id)

    def __init__(self, title):
        self.title = title

    def output_obj(self):
        return {
            'id': self.id,
            'title': self.title,
            'sections': [s.output_obj() for s in self.ordered_sections]
        }

    @property
    def ordered_sections(self):
        return sorted(self.sections, key=lambda section: section.order_in_report)


class Section(db.Model):
    __tablename__ = 'Section'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, index=True, nullable=False)
    context = db.Column(db.Text)
    order_in_report = db.Column(db.Integer, nullable=False, default=0)
    questions = db.relationship('Question', backref='section', lazy='dynamic')
    report_id = db.Column(db.Integer, db.ForeignKey(Report.id))

    def __repr__(self):
        return u'<Section {0}: {1}>'.format(self.id, self.title)

    def __init__(self, title, context=None, order=0):
        self.title = title
        self.context = context
        self.order_in_report = order

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
            'total_score': self.total_score,
            'multiplication_factor': self.multiplication_factor,
            'order_in_report': self.order_in_report,
            'questions': [q.output_obj() for q in self.ordered_questions],
            'report_id': self.report_id,
            'next_section_id': next_section_id,
            'previous_section_id': previous_section_id
        }

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

    @property
    def total_score(self):
        """
        Compute the maximum score for all questions. This is defined as
        score of the answer with the highest score * weight of the question
        :return:
        """
        maximum = 0
        for question in self.questions:
            sorted_answers = sorted(question.answers, key=lambda answer: answer.value)
            sorted_answers.reverse()
            if len(sorted_answers) > 0:
                maximum = maximum + sorted_answers[0].value * question.weight * question.risk_factor.value
        return maximum

    @property
    def multiplication_factor(self):
        if self.total_score == 0:
            # Prevent division by zero errors
            return 100
        else:
            return 100/self.total_score


class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, index=True, nullable=False)
    context = db.Column(db.Text)
    risk = db.Column(db.Text)
    example = db.Column(db.Text)
    weight = db.Column(db.Integer, nullable=False, default=1)
    order_in_section = db.Column(db.Integer, nullable=False, default=0)
    section_id = db.Column(db.Integer, db.ForeignKey(Section.id))
    action = db.Column(db.Text)
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
    question_answers = db.relationship('QuestionAnswer', backref='question_template', lazy='dynamic')
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

    @property
    def highest_answer(self):
        highest = self.answers.order_by('value desc').all()
        return highest[0].value

    def selected_answer(self, user_report_id):
        """
        Returns the selected answer for a specific question in a specific user report
        :param user_report_id:
        :return:
        """
        return QuestionAnswer.query.filter(and_(QuestionAnswer.question_id == self.id,
                                                QuestionAnswer.user_report_id == user_report_id)).first()

    @property
    def maximum_score(self):
        sorted_answers = sorted(self.answers, key=lambda answer: answer.value)
        return sorted_answers[0].value * self.weight * self.risk_factor.value

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
            'maximum_score': self.maximum_score
        }
