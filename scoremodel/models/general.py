from scoremodel import db

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


class Action(db.Model):
    __tablename__ = 'Action'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text, index=True)

    def __repr__(self):
        return '<Action {0}>'.format(self.id)

    def __init__(self, action):
        self.action = action


actions = db.Table('action_question',
                   db.Column('action_id', db.Integer, db.ForeignKey('Action.id')),
                   db.Column('question_id', db.Integer, db.ForeignKey('Question.id'))
                   )


class RiskFactor(db.Model):
    __tablename__ = 'RiskFactor'
    id = db.Column(db.Integer, primary_key=True)
    risk_factor = db.Column(db.Text, index=True, unique=True)

    def __repr__(self):
        return '<RiskFactor {0}>'.format(self.id)

    def __init__(self, risk_factor):
        self.risk_factor = risk_factor


risk_factors = db.Table('riskfactor_question',
                        db.Column('risk_factor_id', db.Integer, db.ForeignKey('RiskFactor.id')),
                        db.Column('question_id', db.Integer, db.ForeignKey('Question.id'))
                        )


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
    actions = db.relationship('Action',
                              secondary=actions,
                              primaryjoin=(actions.c.question_id == id),
                              secondaryjoin=(actions.c.action_id == Action.id),
                              backref=db.backref('questions', lazy='dynamic'),
                              lazy='dynamic'
                              )
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

    def __repr__(self):
        return u'<Question {0}: {1}>'.format(self.id, self.question)

    def __init__(self, question, context=None, risk=None, example=None, weight=1, order=0):
        self.question = question
        self.context = context
        self.risk = risk
        self.example = example
        self.weight = weight
        self.order_in_section = order

    def highest_answer(self):
        highest = self.answers.order_by('value desc').all()
        return highest[0].value


class Section(db.Model):
    __tablename__ = 'Section'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, index=True, nullable=False)
    context = db.Column(db.Text)
    total_score = db.Column(db.Integer, default=0, nullable=False)
    order_in_report = db.Column(db.Integer, nullable=False, default=0)
    questions = db.relationship('Question', backref='section', lazy='dynamic')
    report_id = db.Column(db.Integer, db.ForeignKey(Report.id))

    def __repr__(self):
        return u'<Section {0}: {1}>'.format(self.id, self.title)

    def __init__(self, title, context=None, total_score=0, order=0):
        self.title = title
        self.context = context
        self.total_score = total_score
        self.order_in_report = 0


class Report(db.Model):
    __tablename__ = 'Report'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, index=True, nullable=False)
    sections = db.relationship('Section', backref='report', lazy='dynamic')

    def __repr__(self):
        return '<Report {0}>'.format(self.id)

    def __init__(self, title):
        self.title = title


class Answer(db.Model):
    __tablename__ = 'Answer'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False, index=True)
    value = db.Column(db.Integer, nullable=True, default=1)
    order_in_question = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return u'<Answer {0}: {1}>'.format(self.id, self.answer)

    def __init__(self, answer, value=1, order=0):
        self.answer = answer
        self.value = value
        self.order_in_question = order


answers = db.Table('answer_question',
                   db.Column('answer_id', db.Integer, db.ForeignKey('Answer.id')),
                   db.Column('question_id', db.Integer, db.ForeignKey('Question.id'))
                   )
