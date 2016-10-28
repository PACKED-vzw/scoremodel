from scoremodel.modules.api.organisation_type import OrganisationTypeApi
from scoremodel.modules.api.tests import *
from scoremodel.models.user import OrganisationType


class OrganisationTypeTest(ApiTest):

    def test_create(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        assert ot in scoremodel.db.session
        self.assertRaises(DatabaseItemAlreadyExists, OrganisationTypeApi().create, {'type': 'test'})
        self.assertIsInstance(ot, OrganisationType)

    def test_read(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        assert ot == OrganisationTypeApi().read(ot.id)

    def test_update(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        ot_b = OrganisationTypeApi().update(ot.id, {'type': 'foo'})
        assert ot_b == OrganisationTypeApi().read(ot.id)
        assert OrganisationTypeApi().read(ot.id).type == 'foo'
        self.assertIsInstance(ot_b, OrganisationType)

    def test_delete(self):
        ot = OrganisationTypeApi().create({'type': 'test'})
        assert OrganisationTypeApi().delete(ot.id) is True
        assert ot not in scoremodel.db.session
