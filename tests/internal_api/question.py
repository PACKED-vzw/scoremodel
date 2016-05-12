import pytest
from scoremodel.modules.error import RequiredAttributeMissing
from scoremodel import db
from scoremodel.models.general import Question
from scoremodel.modules.api.question import QuestionApi


def clean():
    pass


def o_test_create_valid():
    clean()
    test_data = {
        'question': 'Py.Test',
        'context': 'Py.Test testing question.',
        'risk': 'Failing would be inconvenient.',
        'example': 'If this fails, it will set an example.',
        'weight': 5,
        'order_in_section': 1,
        'section_id': 1,
        'action': 'If it fails, we will have to go back to the drawing board.',
        'risk_factors': [
            {
                'risk_factor': 'hoog',
                'value': 1
            }
        ],
        'answers': [
            {
                'answer': 'Ja',
                'value': 2
            }
        ]
    }
    qa = QuestionApi()
    with pytest.raises(RequiredAttributeMissing):
        qa.create(test_data)


def test_create_new():
    clean()
    test_data = {
        'question': 'Py.Test',
        'context': 'Py.Test testing question.',
        'risk': 'Failing would be inconvenient.',
        'example': 'If this fails, it will set an example.',
        'weight': 5,
        'order_in_section': 1,
        'section_id': 1,
        'action': 'If it fails, we will have to go back to the drawing board.',
        'risk_factor':
            {
                'risk_factor': 'hoog',
                'value': 1
            }
        ,
        'answers': [
            {
                'answer': 'Ja',
                'value': 2
            }
        ]
    }
    qa = QuestionApi()
    q = qa.create(test_data)
    assert isinstance(q, Question)
    assert qa.delete(q.id) == True


def test_create_update():
    clean()
    test_data = {
        'question': 'Py.Test',
        'context': 'Py.Test testing question.',
        'risk': 'Failing would be inconvenient.',
        'example': 'If this fails, it will set an example.',
        'weight': 5,
        'order_in_section': 1,
        'section_id': 1,
        'action': 'If it fails, we will have to go back to the drawing board.',
        'risk_factor':
            {
                'risk_factor': 'hoog',
                'value': 1
            }
        ,
        'answers': [
            {
                'answer': 'Ja',
                'value': 2
            }
        ]
    }
    qa = QuestionApi()
    q = qa.create(test_data)
    update_data = {
        'question': 'Py.Test',
        'context': 'Py.Test testing question.',
        'risk': 'Failing would be inconvenient. But not fatal.',
        'example': 'If this fails, it will set an example.',
        'weight': 5,
        'order_in_section': 1,
        'section_id': 1,
        'action': 'If it fails, we will have to go back to the drawing board.',
        'risk_factor':
            {
                'risk_factor': 'laag',
                'value': 0
            }
        ,
        'answers': [
            {
                'answer': 'Ja',
                'value': 2
            }
        ]
    }
    q = qa.update(q.id, update_data)
    assert isinstance(q, Question)
    assert qa.delete(q.id) == True
