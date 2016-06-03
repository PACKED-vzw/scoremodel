import bcrypt
from hashlib import sha512
from scoremodel import db
import scoremodel.models.public


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), index=True, unique=True)

    def __repr__(self):
        return '<Role {0}>'.format(self.role)

    def __init__(self, role):
        self.role = role


users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                       )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    questions = db.relationship('QuestionAnswer', backref='user', lazy='dynamic')
    reports = db.relationship('UserReport', backref='user', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)
    locale = db.Column(db.String(8), default='nl')
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
        if bcrypt.hashpw(bit_input, self.password_hash.encode('utf-8')) == self.password_hash.encode('utf-8'):
            return True
        else:
            return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def has_role(self, role_name):
        for role in self.roles:
            if role.role == role_name:
                return True
        return False
