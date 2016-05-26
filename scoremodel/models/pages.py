from scoremodel.models.user import User
from scoremodel import db


class Lang(db.Model):
    __tablename__ = 'Lang'
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(255), index=True)
    pages = db.relationship('Page', backref='lang', lazy='dynamic')

    def __init__(self, lang):
        self.lang = lang

    def __repr__(self):
        return u'<Lang {0}: {1}>'.format(self.id, self.lang)

    def output_obj(self):
        return {
            'lang': self.lang
        }


class MenuLink(db.Model):
    __tablename__ = 'MenuLink'
    id = db.Column(db.Integer, primary_key=True)
    menu_link = db.Column(db.String(255), index=True)
    pages = db.relationship('Page', backref='menu_link', lazy='dynamic')

    def __init__(self, menu_link):
        self.menu_link = menu_link

    def __repr__(self):
        return u'<MenuLink {0}: {1}>'.format(self.id, self.menu_link)

    def output_obj(self):
        return {
            'menu_link': self.menu_link
        }


class Page(db.Model):
    __tablename__ = 'Page'
    id = db.Column(db.Integer, primary_key=True)
    menu_link_id = db.Column(db.Integer, db.ForeignKey(MenuLink.id))
    content = db.Column(db.Text)
    lang_id = db.Column(db.Integer, db.ForeignKey(Lang.id))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return u'<Page {0}: {1}>'.format(self.id, self.menu_link.menu_link)

    def output_obj(self):
        return {
            'id': self.id,
            'menu_link': self.menu_link.menu_link,
            'content': self.content,
            'lang': self.lang.lang
        }
