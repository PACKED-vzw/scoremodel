from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from scoremodel.modules.api.document import DocumentApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.api.file import FileApi
from scoremodel.modules.forms.generic import GenericDeleteForm
from scoremodel.modules.forms.page import PageCreateForm
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist, \
    FileDoesNotExist
from scoremodel.views.admin import admin
from flask_babel import gettext as _


@admin.route('/document/edit/<int:document_id>', methods=['GET'])
@login_required
@must_be_admin
def v_document_edit(document_id):
    document_api = DocumentApi()
    try:
        existing_document = document_api.read(document_id)
    except DatabaseItemDoesNotExist as e:
        flash(_('No document with id {0}').format(document_id))
        return redirect(url_for('admin.v_document_list'))
    except Exception as e:
        flash(_('An unexpected error occurred: {0}').format(e))
        # flash('An unexpected error occurred.')
        return redirect(url_for('admin.v_document_list'))
    lang_api = LangApi()
    languages = lang_api.list()
    return render_template('admin/document/create.html', languages=languages, document=existing_document)


@admin.route('/document/create', methods=['GET'])
@login_required
@must_be_admin
def v_document_create():
    document_id = -1
    lang_api = LangApi()
    languages = lang_api.list()
    return render_template('admin/document/create.html', languages=languages, document={'id': document_id})


@admin.route('/document/list', methods=['GET'])
@login_required
@must_be_admin
def v_document_list():
    document_api = DocumentApi()
    return render_template('admin/document/list.html', documents=document_api.list())


@admin.route('/document/delete/<int:document_id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_document_delete(document_id):
    document_api = DocumentApi()
    form = GenericDeleteForm()
    try:
        existing_document = document_api.read(document_id)
    except DatabaseItemDoesNotExist as e:
        flash(_('No document with id {0}').format(document_id))
        return redirect(url_for('admin.v_document_list'))
    except Exception as e:
        flash(_('An unexpected error occurred: {0}').format(e))
        # flash('An unexpected error occurred.')
        return redirect(url_for('admin.v_document_list'))

    if request.method == 'POST' and form.validate_on_submit():
        # First delete the attached file
        if existing_document.filename and existing_document.filename != '':
            file_api = FileApi()
            try:
                file_api.delete(existing_document.filename)
            except FileDoesNotExist:
                flash(_('Unable to delete attached file. The document was not deleted'))
                return render_template('admin/generic/delete.html', action_url=url_for('admin.v_document_delete',
                                                                                       document_id=document_id),
                                       item_type=_('Document'), item_identifier=document_id, form=form)
        if document_api.delete(document_id) is True:
            flash(_('Document {0} deleted').format(document_id))
            return redirect(url_for('admin.v_document_list'))
        else:
            flash(_('Unable to delete document {0}').format(document_id))
            return render_template('admin/generic/delete.html', action_url=url_for('admin.v_document_delete',
                                                                                   document_id=document_id),
                                   item_type=_('Document'), item_identifier=document_id, form=form)

    return render_template('admin/generic/delete.html', action_url=url_for('admin.v_document_delete',
                                                                           document_id=document_id),
                           item_type=_('Document'), item_identifier=document_id, form=form)
