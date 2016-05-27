from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required
from scoremodel.modules.api.page import PageApi
from scoremodel.modules.api.menu_link import MenuLinkApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.forms.generic import GenericDeleteForm
from scoremodel.modules.forms.page import PageCreateForm
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist
from scoremodel.views.admin import admin
from flask.ext.babel import gettext as _


@admin.route('/document/upload', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_document_upload():
    pass


@admin.route('/document/edit/<int:document_id>', methods=['GET'])
@login_required
@must_be_admin
def v_document_edit(document_id):
    pass


@admin.route('/document/list')
@login_required
@must_be_admin
def v_document_list():
    pass
