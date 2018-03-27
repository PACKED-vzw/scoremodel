from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.modules.api.generic import GenericApi
from scoremodel.models.user import OrganisationType
from scoremodel import db
from scoremodel.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists


class OrganisationTypeApi(GenericApi):
    complex_params = []
    simple_params = ['type']
    required_params = ['type']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        clean_data = self.clean_input(input_data)
        existing_type = OrganisationType.query.filter(OrganisationType.type == clean_data['type']).first()
        if existing_type:
            raise DatabaseItemAlreadyExists(_e['item_exists'].format(OrganisationType, clean_data['type']))
        new_type = OrganisationType(type=clean_data['type'])
        db.session.add(new_type)
        db.session.commit()
        return new_type

    def read(self, type_id):
        existing_type = OrganisationType.query.filter(OrganisationType.id == type_id).first()
        if not existing_type:
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(OrganisationType, type_id))
        return existing_type

    def update(self, type_id, input_data):
        clean_data = self.clean_input(input_data)
        existing_type = self.read(type_id)
        existing_type = self.update_simple_attributes(existing_type, self.simple_params, clean_data)
        db.session.commit()
        return existing_type

    def delete(self, type_id):
        existing_type = self.read(type_id)
        db.session.delete(existing_type)
        db.session.commit()
        return True

    def list(self):
        all_types = OrganisationType.query.all()
        return all_types

    def clean_input(self, unclean_data):
        cleaned_data = self.clean_input_data(OrganisationType, unclean_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        return cleaned_data
