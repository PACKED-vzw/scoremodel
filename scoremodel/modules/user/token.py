import string
import random


class Token:

    def __init__(self):
        self.size = 64
        self.chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

    def token(self, size=None):
        if not size:
            size = self.size
        return ''.join(random.choice(self.chars) for _ in range(size))

    def unique_token(self, db_class, attr_name, size=None):
        if not size:
            size = self.size
        token = self.token(size)
        while db_class.query.filter(getattr(db_class, attr_name) == token).first() is not None:
            token = self.token(size)
        return token
