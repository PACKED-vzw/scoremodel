import bcrypt
from hashlib import sha512
from scoremodel import db, app
import scoremodel.models.public
from flask_login import AnonymousUserMixin
from scoremodel.modules.user.token import Token


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(190), index=True, unique=True)

    def __repr__(self):
        return '<Role {0}>'.format(self.role)

    def __init__(self, role):
        self.role = role


users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                       )


class OrganisationType(db.Model):
    __tablename__ = 'OrganisationType'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(190), index=True, unique=True)
    organisations = db.relationship('Organisation', backref='type', lazy='dynamic')

    def __init__(self, type):
        self.type = type


class Organisation(db.Model):
    __tablename__ = 'Organisation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    type_id = db.Column(db.Integer, db.ForeignKey(OrganisationType.id))
    size = db.Column(db.String(255))
    users = db.relationship('User', backref='organisation', lazy='dynamic')

    def __init__(self, name, size=None):
        self.name = name
        if size:
            self.size = size


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(190), index=True, unique=True, nullable=False)
    email = db.Column(db.String(190), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    questions = db.relationship('QuestionAnswer', backref='user', lazy='dynamic')
    reports = db.relationship('UserReport', backref='user', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)
    lang_id = db.Column(db.Integer, db.ForeignKey('Lang.id'))
    api_key = db.Column(db.String(190), nullable=False, unique=True)
    session_token = db.Column(db.String(190), nullable=False, unique=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id))
    roles = db.relationship('Role',
                            secondary=users_roles,
                            primaryjoin=(users_roles.c.user_id == id),
                            secondaryjoin=(users_roles.c.role_id == Role.id),
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.username = self.email
        self.set_password(password)
        self.set_api_key()
        self.set_session_token()

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def output_obj(self):
        return {
            'id': self.id,
            'username': self.username,
            'posts': [p.id for p in self.posts],
            'roles': [r.id for r in self.roles]
        }

    def set_password(self, input_password):
        bit_input = input_password.encode('utf-8')
        self.password_hash = bcrypt.hashpw(bit_input, bcrypt.gensalt())

    def verify_password(self, input_password):
        bit_input = input_password.encode('utf-8')
        # Check needed because mysql returns strings (in unicode), but sqlite returns bits
        if isinstance(self.password_hash, str):
            password_hash = self.password_hash.encode('utf-8')
        else:
            password_hash = self.password_hash
        if bcrypt.hashpw(bit_input, password_hash) == password_hash:
            return True
        else:
            return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """
        Returns the session_token, not the ID (see #Alternative Tokens at https://flask-login.readthedocs.io/en/latest/)
        :return:
        """
        return self.session_token

    def is_authenticated(self):
        return self.authenticated

    def has_role(self, role_name):
        for role in self.roles:
            if role.role == role_name:
                return True
        return False

    def set_api_key(self):
        self.api_key = Token().unique_token(User, 'api_key', 64)

    def set_session_token(self):
        self.session_token = Token().unique_token(User, 'session_token', 64)

    @property
    def locale(self):
        if self.lang:
            return self.lang.lang
        return app.config['BABEL_DEFAULT_LOCALE']

