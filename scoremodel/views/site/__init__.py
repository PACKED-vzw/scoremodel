from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from flask_login import login_required, current_user
from flask_babel import gettext as _
import markdown

from scoremodel.modules.api.page import PageApi
from scoremodel.modules.api.document import DocumentApi
from scoremodel.modules.user.authentication import LoginForm
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.modules.api.user import UserApi
from scoremodel.modules.locale import Locale
from scoremodel import app

site = Blueprint('site', __name__, url_prefix='/site')

page_api = PageApi()
locale_api = Locale()


@site.route('/')
@site.route('/home')
def v_index():
    form = LoginForm()
    user_api = UserApi()
    lang = locale_api.current_locale
    if current_user and current_user.is_authenticated:
        user_reports = user_api.get_user_reports(current_user.id)
    else:
        user_reports = []
    try:
        page = page_api.by_menu_link_and_lang('v_index', lang)
    except DatabaseItemDoesNotExist:
        try:
            page = page_api.by_menu_link_and_lang('v_index', app.config['BABEL_DEFAULT_LOCALE'])
        except DatabaseItemDoesNotExist:
            abort(404)
            return
    return render_template('site/home.html', form=form, content=markdown.markdown(page.content),
                           user_reports=user_reports[:5])


@site.route('/faq')
def v_faq():
    lang = locale_api.current_locale
    try:
        page = page_api.by_menu_link_and_lang('v_faq', lang)
    except DatabaseItemDoesNotExist:
        try:
            page = page_api.by_menu_link_and_lang('v_faq', app.config['BABEL_DEFAULT_LOCALE'])
        except DatabaseItemDoesNotExist:
            abort(404)
            return
    return render_template('site/content.html', content=markdown.markdown(page.content), title=_('FAQ'))


@site.route('/documents')
def v_doc():
    document_api = DocumentApi()
    lang = locale_api.current_locale
    documents = document_api.by_lang(lang)
    return render_template('site/documents.html', documents=documents, title=_('Documents'))


@site.route('/disclaimer')
def v_disclaimer():
    lang = locale_api.current_locale
    try:
        page = page_api.by_menu_link_and_lang('v_disclaimer', lang)
    except DatabaseItemDoesNotExist:
        try:
            page = page_api.by_menu_link_and_lang('v_disclaimer', app.config['BABEL_DEFAULT_LOCALE'])
        except DatabaseItemDoesNotExist:
            abort(404)
            return
    return render_template('site/content.html', content=markdown.markdown(page.content), title=_('Disclaimer'))


@site.route('/contact')
def v_contact():
    lang = locale_api.current_locale
    try:
        page = page_api.by_menu_link_and_lang('v_contact', lang)
    except DatabaseItemDoesNotExist:
        try:
            page = page_api.by_menu_link_and_lang('v_contact', app.config['BABEL_DEFAULT_LOCALE'])
        except DatabaseItemDoesNotExist:
            abort(404)
            return
    return render_template('site/content.html', content=markdown.markdown(page.content), title=_('Contact'))
