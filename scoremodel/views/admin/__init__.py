from flask import render_template
from flask.ext.login import login_required
from scoremodel.modules.user.authentication import role_required
from scoremodel import app


@app.route('/admin')
@login_required
@role_required('administrator')
def v_admin():
    return render_template('admin/generic/index.html')

