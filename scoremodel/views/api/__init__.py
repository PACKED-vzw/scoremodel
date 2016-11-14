import json

from flask import Blueprint
from scoremodel.modules.api.rest import RestApi
from scoremodel.modules.locale import Locale
from scoremodel import csrf

api = Blueprint('api', __name__, url_prefix='/api/v2')

import scoremodel.views.api.report
import scoremodel.views.api.user_report
import scoremodel.views.api.report.benchmark
import scoremodel.views.api.page


@csrf.exempt
@api.route('/locale/<string:locale_name>', methods=['POST'])
@api.route('/locale', methods=['GET'])
def v_set_locale(locale_name=None):
    locale_api = Locale()
    rest_api = RestApi()
    data = u''
    if not locale_name:
        status_code = 200
        data = {'locale': locale_api.current_locale}
    else:
        if locale_api.set_locale(locale_name) is True:
            status_code = 200
        else:
            status_code = 400
    return rest_api.response(status=status_code, data=data)
