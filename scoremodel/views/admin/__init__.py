from flask import render_template, Blueprint
from flask_login import login_required
from scoremodel.modules.user.authentication import role_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

from scoremodel.views.admin.answer import *
from scoremodel.views.admin.auth import *
from scoremodel.views.admin.report import *
from scoremodel.views.admin.risk_factor import *
from scoremodel.views.admin.user import *
from scoremodel.views.admin.page import *
from scoremodel.views.admin.document import *
from scoremodel.views.admin.organisation_type import *


@admin.route('/')
@login_required
@role_required('administrator')
def v_admin():
    return render_template('admin/generic/index.html')

