from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.modules.api.generic import GenericApi
from scoremodel.models.user import Organisation
from scoremodel.modules.api.organisation_type import OrganisationTypeApi
from scoremodel import db
from scoremodel.modules.error import DatabaseItemDoesNotExist


class OrganisationApi(GenericApi):
    complex_params = []
    simple_params = ['name', 'type_id', 'size']
    required_params = ['name', 'type_id']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        clean_data = self.clean_input(input_data)
        new_organisation = Organisation(name=clean_data['name'])
        # There can be multiple organisations with the same name; this is autocreated with new users and is purely
        # informational.
        existing_type = OrganisationTypeApi().read(clean_data['type_id'])
        new_organisation.type = existing_type
        db.session.add(new_organisation)
        db.session.commit()
        return new_organisation

    def read(self, organisation_id):
        existing_organisation = Organisation.query.filter(Organisation.id == organisation_id).first()
        if not existing_organisation:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(Organisation, organisation_id))
        return existing_organisation

    def update(self, organisation_id, input_data):
        clean_data = self.clean_input(input_data)
        existing_organisation = self.read(organisation_id)
        existing_organisation = self.update_simple_attributes(existing_organisation, self.simple_params, clean_data,
                                                              to_skip=['type_id'])
        existing_type = OrganisationTypeApi().read(clean_data['type_id'])
        existing_organisation.type = existing_type
        db.session.commit()
        return existing_organisation

    def delete(self, organisation_id):
        existing_organisation = self.read(organisation_id)
        db.session.delete(existing_organisation)
        db.session.commit()
        return True

    def list(self):
        existing_organisations = Organisation.query.all()
        return existing_organisations

    def clean_input(self, unclean_data):
        cleaned_data = self.clean_input_data(Organisation, unclean_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        return cleaned_data
