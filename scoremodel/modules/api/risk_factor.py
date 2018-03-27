from flask_babel import gettext as _
from scoremodel.modules.msg.messages import module_error_msg as _e
from scoremodel.models.general import RiskFactor
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.lang import LangApi
from scoremodel import db


class RiskFactorApi(GenericApi):
    complex_params = []
    simple_params = ['risk_factor', 'value', 'lang_id']
    possible_params = ['risk_factor', 'value', 'lang_id']
    required_params = ['risk_factor', 'lang_id']

    def __init__(self, risk_factor_id=None):
        self.risk_factor_id = risk_factor_id
        self.lang_api = LangApi()

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
            raise DatabaseItemAlreadyExists(_e['item_exists']
                                            .format(RiskFactor, cleaned_data['risk_factor']))
        new_risk_factor = RiskFactor(**cleaned_data)
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
            raise DatabaseItemDoesNotExist(_e['item_not_exists'].format(RiskFactor, risk_factor_id))
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

    def by_lang(self, lang):
        """
        List all in a given language
        :return:
        """
        existing_lang = self.lang_api.by_lang(lang)
        existing_reports = RiskFactor.query.filter(RiskFactor.lang_id == existing_lang.id).all()
        return existing_reports

    def parse_input_data(self, input_data):
        return self.clean_input_data(RiskFactor, input_data, self.possible_params, self.required_params,
                                     self.complex_params)
