from scoremodel.modules.api.organisation import OrganisationApi
from scoremodel.modules.api.organisation_type import OrganisationTypeApi
from scoremodel.modules.api.tests import *
from scoremodel.models.user import Organisation


class OrganisationTest(ApiTest):

    def test_create(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        o = OrganisationApi().create({'name': 'foo', 'type_id': ot.id})
        assert o in scoremodel.db.session
        self.assertIsInstance(o, Organisation)

    def test_read(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        o = OrganisationApi().create({'name': 'foo', 'type_id': ot.id})
        assert o == OrganisationApi().read(o.id)

    def test_update(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        o = OrganisationApi().create({'name': 'foo', 'type_id': ot.id})
        o_b = OrganisationApi().update(o.id, {'name': 'bar', 'type_id': ot.id})
        assert o_b == OrganisationApi().read(o.id)
        assert OrganisationApi().read(o.id).name == 'bar'
        self.assertIsInstance(o_b, Organisation)

    def test_delete(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        o = OrganisationApi().create({'name': 'foo', 'type_id': ot.id})
        assert OrganisationApi().delete(o.id) is True
        assert o not in scoremodel.db.session
