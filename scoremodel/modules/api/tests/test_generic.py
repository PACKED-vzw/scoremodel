from scoremodel.modules.api.tests import *


class GenericTest(ApiTest):

    f_to_test = ('test_create', 'test_read', 'test_update', 'test_delete')
    c_to_test = ('answer', 'document', 'lang', 'menu_link', 'organisation', 'organisation_type', 'page', 'question',
                 'risk_factor', 'role', 'score', 'section', 'user', 'user_report')
