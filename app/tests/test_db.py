""" Test DB API using fake data, mocking, patching and vcr
Example adapted from:
https://github.com/miguendes/tutorials/blob/master/testing_http/tests/test_weather_app.py
"""

from typing import Dict, Any
import json
from http import HTTPStatus
import pytest
import vcr
from db_api import insert_one
from db_api import insert_many
from db_api import find_one


@pytest.fixture()
def fake_mongo_db() -> Dict[str, Any]:
    """Fixture that returns fake recipes.
    """
    recipes: Dict[str, Any] = {}
    with open('app/tests/resources/recipes.json', encoding='utf-8') as f:
        recipes = json.load(f)

    return recipes


def update_fake_mongo_db(recipes: Dict[str, Any]) -> None:
    """Fixture that updates fake recipes.
    """
    with open('app/tests/resources/recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=4)

# fixture are passed as arguments to the test functions


def test_find_one(mocker: Any, fake_mongo_db: Dict[str, Any]) -> None:
    """Test find_one function.
    """
    fake_response = mocker.Mock()
    fake_response.status_code = HTTPStatus.OK
    where = {'name': 'Spanish Omelet'}
    for doc in fake_mongo_db['documents']:
        if doc['name'] == 'Spanish Omelet':
            fake_response.json.return_value = doc
            break
    mocker.patch(__name__ + '.find_one', return_value=fake_response)
    recipe = find_one(where).json()
    assert recipe['name'] == 'Spanish Omelet'


@vcr.use_cassette()
def test_find_one_using_vcr() -> None:
    """Mocking with VCR.
        Creates a cassette (yaml) with the response from the API.
        If the cassette already exists, it will use it.
    """
    where = {'name': 'Spanish Omelet'}
    recipe = find_one(where)['document']
    print(recipe)
    assert recipe['name'] == 'Spanish Omelet'


def test_insert_one(mocker: Any, fake_mongo_db: Dict[str, Any]) -> None:
    """Test insert_one function.
    Args:
        mocker (Any): pytest-mock fixture.
        fake_mongo_db (Dict[str, Any]): Fake recipes fixture.
    """
    recipe = {
        'name': 'Spanish scrambled eggs',
        'ingredients': ['eggs', 'onion', 'potatoes'],
        'steps': ['step 1', 'step 2', 'step 3'],
        'prep_time': 10,
        'difficulty': 'easy'
    }
    fake_response = mocker.Mock()
    fake_response.status_code = 201
    fake_response.json.return_value = {
        'insertedId': '5f7b1a7d3a9f8e6d0e3e5e2c'
    }
    mocker.patch(__name__ + '.insert_one', return_value=fake_response)
    response = insert_one(recipe)
    fake_mongo_db['documents'].append(recipe)
    # update_fake_mongo_db(fake_mongo_db)
    assert response.status_code == 201
    assert response.json()['insertedId'] is not None


def test_insert_many(mocker: Any, fake_mongo_db: Dict[str, Any]) -> None:
    """Test insert_many function.

    Args:
        mocker (Any): pytest-mock fixture.
        fake_mongo_db (Dict[str, Any]): Fake recipes fixture.
    """
    recipes = [
        {
            'name': 'Spanish boiled eggs',
            'ingredients': ['eggs', 'onion', 'potatoes'],
            'steps': ['step 1', 'step 2', 'step 3'],
            'prep_time': 15,
            'difficulty': 'easy'
        },
        {
            'name': 'Spanish sunny side up eggs',
            'ingredients': ['eggs', 'onion', 'potatoes'],
            'steps': ['step 1', 'step 2', 'step 3'],
            'prep_time': 10,
            'difficulty': 'easy'
        }
    ]
    fake_response = mocker.Mock()
    fake_response.status_code = 201
    fake_response.json.return_value = {
        'insertedIds': ['5f7b1a7d3a9f8e6d0e3e5e2c', '5f7b1a7d3a9f8e6d0e3e5e2d']
    }
    mocker.patch(__name__ + '.insert_many', return_value=fake_response)
    response = insert_many(recipes)
    fake_mongo_db['documents'].extend(recipes)
    # update_fake_mongo_db(fake_mongo_db)
    assert response.status_code == 201
    assert response.json()['insertedIds'] is not None
    assert len(response.json()['insertedIds']) == 2
