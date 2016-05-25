from scoremodel.models.user import User
from scoremodel import db


class Page(db.Model):
    __tablename__ = 'Page'
    id = db.Column(db.Integer, primary_key=True)
    menu_link = db.Column(db.String(255), index=True)
    content = db.Column(db.Text)
    lang = db.Column(db.String(8), default='nl', index=True)

    def __init__(self, menu_link, content, lang=None):
        self.menu_link = menu_link
        self.content = content
        if lang:
            self.lang = lang

    def __repr__(self):
        return u'<Page {0}: {1}>'.format(self.id, self.menu_link)

    def output_obj(self):
        return {
            'id': self.id,
            'menu_link': self.menu_link,
            'content': self.content,
            'lang': self.lang
        }
