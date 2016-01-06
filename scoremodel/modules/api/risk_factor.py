from scoremodel.models.general import RiskFactor
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel import db


class RiskFactorApi(GenericApi):
    complex_params = []
    simple_params = ['risk_factor']

    def __init__(self, risk_factor_id=None):
        self.risk_factor_id = risk_factor_id

    def create(self, input_data):
        """
        Create a new RiskFactor. See QuestionApi.create(). Fails when the risk factor already exists.
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        try:
            existing_risk_factor = self.get_risk_factor(cleaned_data['risk_factor'])
        except DatabaseItemDoesNotExist:
            existing_risk_factor = None
        if existing_risk_factor:
            raise DatabaseItemAlreadyExists('A risk factor called "{0}" already exists.'
                                            .format(cleaned_data['risk_factor']))
        new_risk_factor = RiskFactor(cleaned_data['risk_factor'])
        db.session.add(new_risk_factor)
        db.session.commit()
        return new_risk_factor

    def read(self, risk_factor_id):
        """
        Return a RiskFactor by its id. See QuestionApi.read()
        :param risk_factor_id:
        :return:
        """
        existing_risk_factor = RiskFactor.query.filter(RiskFactor.id == risk_factor_id).first()
        if existing_risk_factor is None:
            raise DatabaseItemDoesNotExist('No risk factor with id {0}'.format(risk_factor_id))
        return existing_risk_factor

    def update(self, risk_factor_id, input_data):
        """
        Update an existing RiskFactor. See QuestionApi.update()
        :param risk_factor_id:
        :param input_data:
        :return:
        """
        cleaned_data = self.parse_input_data(input_data)
        existing_risk_factor = self.read(risk_factor_id)
        existing_risk_factor = self.update_simple_attributes(existing_risk_factor, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_risk_factor

    def delete(self, risk_factor_id):
        """
        Delete an existing RiskFactor. See QuestionApi.delete()
        :param risk_factor_id:
        :return:
        """
        existing_risk_factor = self.read(risk_factor_id)
        db.session.delete(existing_risk_factor)
        db.session.commit()
        return True

    def list(self):
        """
        List all risk_factors
        :return:
        """
        risk_factors = RiskFactor.query.all()
        return risk_factors

    def parse_input_data(self, input_data):
        possible_params = ['risk_factor']
        required_params = ['risk_factor']
        return self.clean_input_data(RiskFactor, input_data, possible_params, required_params, self.complex_params)
