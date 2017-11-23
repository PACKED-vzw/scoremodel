from scoremodel import app, db
from scoremodel.models.general import RiskFactor, Report, Answer, Question, Section, Benchmark, BenchmarkReport
from scoremodel.models.public import UserReport, QuestionAnswer
from scoremodel.models.user import Role, User, Organisation, OrganisationType
from scoremodel.models.pages import Page, Document, Lang, MenuLink
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.api.role import RoleApi
from scoremodel.modules.api.menu_link import MenuLinkApi
from scoremodel.modules.error import DatabaseItemDoesNotExist
from random import SystemRandom
from sqlalchemy.exc import OperationalError, NoSuchTableError, ProgrammingError
from sqlalchemy import Table, MetaData
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
    tables = ('Answer', 'Section', 'Question', 'Report', 'BenchmarkReport', 'Benchmark', 'RiskFactor',
              'Lang', 'MenuLink', 'Page', 'Document',
              'UserReport', 'QuestionAnswer',
              'Role', 'User', 'Organisation', 'OrganisationType')
    for table in tables:
        try:
            o_t = eval(table)
            t = o_t.query.all()
        except NoSuchTableError:
            return False
        except OperationalError:
            return False
        except ProgrammingError:
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
        try:
            role_api.get_by_role(role)
        except DatabaseItemDoesNotExist:
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
    try:
        user_api.get_by_user('admin@packed.be')
    except DatabaseItemDoesNotExist:
        admin = user_api.create(user_data)
        return {
            'user': admin,
            'password': user_data['password']
        }


def add_menu_links():
    menu_links = ('v_index', 'v_faq', 'v_disclaimer', 'v_doc', 'v_contact')
    menu_link_api = MenuLinkApi()
    for menu_link in menu_links:
        try:
            menu_link_api.by_menu_link(menu_link)
        except DatabaseItemDoesNotExist:
            menu_link_api.create({'menu_link': menu_link})


def add_lang():
    languages = app.config['LANGUAGES']
    lang_api = LangApi()
    if len(languages) == 0:
        languages.append('en')
    for lang in languages:
        try:
            lang_api.by_lang(lang)
        except DatabaseItemDoesNotExist:
            lang_api.create({'lang': lang})


def testing_db_setup():
    add_tables()
    add_roles()
    add_lang()
    add_menu_links()
    if not check_has_admin():
        adm = add_admin()
        return adm
    return True

