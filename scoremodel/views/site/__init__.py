from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _
import markdown

from scoremodel.modules.api.page import PageApi
from scoremodel.modules.user.authentication import LoginForm
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.modules.api.user import UserApi

site = Blueprint('site', __name__, url_prefix='/site')

page_api = PageApi()
# TODO: lang
lang = 'nl'


@site.route('/')
@site.route('/home')
def v_index():
    form = LoginForm()
    user_api = UserApi()
    if current_user and current_user.is_authenticated:
        user_reports = user_api.get_user_reports(current_user.id)
    else:
        user_reports = []
    try:
        page = page_api.by_menu_link_and_lang('v_index', lang)
    except DatabaseItemDoesNotExist:
        abort(404)
        return
    return render_template('site/home.html', form=form, content=markdown.markdown(page.content),
                           user_reports=user_reports)


@site.route('/faq')
def v_faq():
    try:
        page = page_api.by_menu_link_and_lang('v_faq', lang)
    except DatabaseItemDoesNotExist:
        abort(404)
        return
    return render_template('site/content.html', content=markdown.markdown(page.content), title=_('FAQ'))


@site.route('/documents')
def v_doc():
    pass


@site.route('/disclaimer')
def v_disclaimer():
    try:
        page = page_api.by_menu_link_and_lang('v_disclaimer', lang)
    except DatabaseItemDoesNotExist:
        abort(404)
        return
    return render_template('site/content.html', content=markdown.markdown(page.content), title=_('Disclaimer'))
