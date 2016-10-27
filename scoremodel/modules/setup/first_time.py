from scoremodel import app, db
from scoremodel.models.general import RiskFactor, Report, Answer, Question, Section
from scoremodel.models.public import UserReport, QuestionAnswer
from scoremodel.models.user import Role, User
from scoremodel.models.pages import Page, Document, Lang, MenuLink
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.role import RoleApi
from scoremodel.modules.api.menu_link import MenuLinkApi
from random import SystemRandom
from sqlalchemy.exc import OperationalError
import string

##
# Functions to perform the first time setup
##


def add_tables():
    db.create_all()


def check_has_tables():
    """
    If we get an OperationalError, the tables do not yet exist.
    :return:
    """
    try:
        users = User.query.all()
    except OperationalError:
        return False
    return True


def check_has_admin():
    """
    If there are no users, this is the first run of the application.
    :return:
    """
    user_api = UserApi()
    if len(user_api.list()) > 0:
        return True
    else:
        return False


def add_roles():
    minimal_roles = ('administrator', 'public')
    role_api = RoleApi()
    for role in minimal_roles:
        role_api.create({'role': role})


def add_admin():
    user_api = UserApi()
    role_api = RoleApi()
    admin_role = role_api.get_by_role('administrator')
    if app.config['DEBUG'] is True:
        password = 'admin'
    else:
        password = ''.join(SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    user_data = {
        'email': 'admin@packed.be',
        'password': password,
        'roles': [
            admin_role.id
        ]
    }
    admin = user_api.create(user_data)
    return {
        'user': admin,
        'password': user_data['password']
    }


def add_menu_links():
    menu_links = ('v_index', 'v_faq', 'v_disclaimer', 'v_doc')
    menu_link_api = MenuLinkApi()
    for menu_link in menu_links:
        menu_link_api.create({'menu_link': menu_link})


def add_lang():
    languages = app.config['LANGUAGES']
    lang_api = LangApi()
    if len(languages) == 0:
        languages.append('en')
    for lang in languages:
        lang_api.create({'lang': lang})


def testing_db_setup():
    if not check_has_tables():
        add_tables()
        add_roles()
        add_lang()
        add_menu_links()
    if not check_has_admin():
        adm = add_admin()
        return adm
    return True

