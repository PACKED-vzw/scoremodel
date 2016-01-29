from flask import redirect, url_for, render_template, flash
from scoremodel.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing


class ScoremodelAdminGui:

    def __init__(self, c_form, o_request, c_api, error_view, success_view=None):
        """
        Generic Admin GUI.
        :param c_form: class of the form used for this administrative function (e.g. UserCreateForm)
        :param o_request: request object.
        :param c_api: class of the api (e.g. UserApi) - from helptux.modules.api
        :param error_view: string containing the name of the functions for the view we have to redirect to in case of
                an error.
        :param success_view: like error_view, but in case of success.
        :return:
        """
        self.form = c_form()
        self.request = o_request
        self.api = c_api()
        self.error_view = error_view
        if not success_view:
            success_view = self.error_view
        self.success_view = success_view

    def log(self, msg):
        # TODO: implement logger module
        print(msg)

    def create(self, template, form_vars=(), template_opts=None):
        """
        Create an item using self.api, which is from helptux.modules.api.
        :param template: location (string) of the jinja template for this action.
        :param form_vars: variables (attributes of self.form) this function has to fetch from the returned form.
        :param template_opts: additional options for render_template
        :return: rendered template or redirect
        """
        if self.request.method == 'POST' and self.form.validate_on_submit():
            input_data = {}
            for form_var in form_vars:
                input_data[form_var] = self.form[form_var].data
            # Create using the API
            try:
                created_item = self.api.create(input_data)
            except DatabaseItemAlreadyExists as e:
                flash('Failed to create this item: {0}'.format(e))
                return redirect(url_for(self.error_view))
            except RequiredAttributeMissing as e:
                flash('Required variable missing: {0}'.format(e))
                return redirect(url_for(self.error_view))
            except Exception as e:
                flash('An unexpected error occurred. Check the log.')
                self.log(e)
                return redirect(url_for(self.error_view))
            else:
                flash('Item created successfully.')
                return redirect(url_for(self.success_view))
        else:
            # Form has not yet been submitted
            return render_template(template, form=self.form, **template_opts)
