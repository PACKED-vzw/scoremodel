from scoremodel import app
from flask import request, make_response, render_template


# TODO authentication
@app.route('/admin/type/report/', methods=['GET'])
@app.route('/admin/type/report/id/<int:report_id>/', methods=['GET'])
def report_admin(report_id=None):
    return render_template('admin/report.html')


##
# Helpers (TODO?)
##
