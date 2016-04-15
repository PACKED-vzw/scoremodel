import pytest
from scoremodel.modules.api.risk_factor import RiskFactorApi
from scoremodel.models.general import RiskFactor
from scoremodel.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing
from scoremodel.modules.setup import AppSetup


def setup_module():
    pass


def test_create_valid():
    data_structure = {
        'risk_factor': 'medium'
    }
    risk_factor_api = RiskFactorApi()
    risk_factor = risk_factor_api.create(data_structure)
    assert(type(risk_factor) == RiskFactor)
    assert(risk_factor_api.delete(risk_factor.id) == True)


def test_create_empty():
    data_structure = {}
    risk_factor_api = RiskFactorApi()
    with pytest.raises(RequiredAttributeMissing):
        risk_factor_api.create(data_structure)


def test_create_invalid():
    data_structure = {
        'risk_factor': 'nauhatl',
        'nobody': True
    }
    risk_factor_api = RiskFactorApi()
    risk_factor = risk_factor_api.create(data_structure)
    assert (type(risk_factor) == RiskFactor)
    assert (risk_factor_api.delete(risk_factor.id) == True)


def test_create_complete():
    data_structure = {
        'risk_factor': 'medium',
        'value': 2
    }
    risk_factor_api = RiskFactorApi()
    risk_factor = risk_factor_api.create(data_structure)
    assert(type(risk_factor) == RiskFactor)
    assert(risk_factor_api.delete(risk_factor.id) == True)


def test_create_update():
    data_structure = {
        'risk_factor': 'zeer hoog',
        'value': 5
    }
    risk_factor_api = RiskFactorApi()
    risk_factor = risk_factor_api.create(data_structure)
    assert (type(risk_factor) == RiskFactor)
    updated_data = {
        'risk_factor': 'bijzonder hoog',
        'value': 5
    }
    updated = risk_factor_api.update(risk_factor.id, updated_data)
    assert(type(updated) == RiskFactor)
    assert(updated.risk_factor == 'bijzonder hoog')
    assert (risk_factor_api.delete(updated.id) == True)


def test_create_delete():
    data_structure = {
        'risk_factor': 'zeer hoog',
        'value': 5
    }
    risk_factor_api = RiskFactorApi()
    risk_factor = risk_factor_api.create(data_structure)
    assert (type(risk_factor) == RiskFactor)
    assert (risk_factor_api.delete(risk_factor.id) == True)
    with pytest.raises(DatabaseItemDoesNotExist):
        risk_factor_api.read(risk_factor.id)
