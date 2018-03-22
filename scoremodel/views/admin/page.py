from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from scoremodel.modules.api.page import PageApi
from scoremodel.modules.api.menu_link import MenuLinkApi
from scoremodel.modules.api.lang import LangApi
from scoremodel.modules.forms.generic import GenericDeleteForm
from scoremodel.modules.forms.page import PageCreateForm
from scoremodel.modules.error import DatabaseItemDoesNotExist
from scoremodel.modules.user.authentication import must_be_admin
from scoremodel.modules.error import DatabaseItemAlreadyExists, RequiredAttributeMissing, DatabaseItemDoesNotExist
from scoremodel.views.admin import admin
from flask_babel import gettext as _

page_api = PageApi()
lang_api = LangApi()
menu_link_api = MenuLinkApi()


@admin.route('/page/create', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_page_create():
    form = PageCreateForm()
    form.lang.choices = [(l.id, l.lang) for l in lang_api.list()]
    form.menu_link.choices = [(m.id, m.menu_link) for m in menu_link_api.list()]
    if request.method == 'POST' and form.validate_on_submit():
        page_data = {
            'menu_link_id': form.menu_link.data,
            'lang_id': form.lang.data
        }
        try:
            new_page = page_api.create(page_data)
        except DatabaseItemAlreadyExists as e:
            flash(_('This page already exists.'))
            return redirect(url_for('admin.v_page_create'))
        except RequiredAttributeMissing as e:
            flash(_('A required form element was not submitted: {0}').format(e))
            return redirect(url_for('admin.v_page_create'))
        except Exception as e:
            flash(_('An unexpected error occurred.'))
            return redirect(url_for('admin.v_page_create'))
        else:
            flash(_('Page created'))
            return redirect(
                url_for('admin.v_page_edit', page_id=new_page.id))
    else:
        return render_template('admin/page/create.html', title=_('Page'), form=form)


@admin.route('/page/edit/<int:page_id>', methods=['GET'])
@login_required
@must_be_admin
def v_page_edit(page_id):
    try:
        existing_page = page_api.read(page_id)
    except DatabaseItemDoesNotExist as e:
        flash(_('No page with id {0}').format(page_id))
        return redirect(url_for('admin.v_page_list'))
    except Exception as e:
        flash(_('An unexpected error occurred: {0}').format(e))
        return redirect(url_for('admin.v_page_list'))
    return render_template('admin/page/edit.html', title=_('Page'), page=existing_page)


@admin.route('/page/delete/<int:page_id>', methods=['GET', 'POST'])
@login_required
@must_be_admin
def v_page_delete(page_id):
    form = GenericDeleteForm()
    try:
        existing_page = page_api.read(page_id)
    except DatabaseItemDoesNotExist as e:
        flash(_('No page with id {0}').format(page_id))
        return redirect(url_for('admin.v_page_list'))
    except Exception as e:
        flash(_('An unexpected error occurred: {0}').format(e))
        # flash('An unexpected error occurred.')
        return redirect(url_for('admin.v_page_list'))

    if request.method == 'POST' and form.validate_on_submit():
        if page_api.delete(page_id) is True:
            flash(_('Page {0} deleted').format(page_id))
            return redirect(url_for('admin.v_page_list'))
        else:
            flash(_('Unable to delete page {0}').format(page_id))
            return render_template('admin/generic/delete.html', action_url=url_for('admin.v_page_delete',
                                                                                   page_id=page_id),
                                   item_type=_('Page'), item_identifier=page_id, form=form)

    return render_template('admin/generic/delete.html', action_url=url_for('admin.v_page_delete',
                                                                           page_id=page_id),
                           item_type=_('Page'), item_identifier=page_id, form=form)


@admin.route('/page', methods=['GET'])
@login_required
@must_be_admin
def v_page_list():
    pages = page_api.list()
    return render_template('admin/page/list.html', title=_('Pages'), pages=pages)
