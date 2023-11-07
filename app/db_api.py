"""
MongoDB database APIs.
"""
import copy
from typing import Dict, List, Any
import requests
# from pymongo import MongoClient

END_POINT = 'https://us-west-2.aws.data.mongodb-api.com/app/'
END_POINT += 'data-whziv/endpoint/data/v1/action'
API_KEY = 'sZSPFtn4h57mJ52S0h9XWzTKJATvieufXuzvgaZBpgL4ybha1vmw6HHksEAzREbi'
DATA_SOURCE = 'Cluster0'
DB_NAME = 'recipe'
COLLECTION = 'spanish'


HEADERS = headers = {'Content-Type': 'application/json',
                     'Access-Control-Request-Headers': '*',
                     'api-key': f'{API_KEY}'}

PAYLOAD = {
    "collection": COLLECTION,
    "database": DB_NAME,
    "dataSource": DATA_SOURCE
}


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session

# let's create our own API function to insert one recipe


def insert_one(recipe: Dict[str, Any]) -> 'requests.Response':
    """Insert one recipe into the database.

    Args:
        recipe (Dict[str, Any]): Recipe to insert.

    Returns:
        requests.Response: Response from the API.
    """
    session = create_session()
    action = f'{END_POINT}/insertOne'
    print(action)
    payload: Dict[str, Any] = copy.deepcopy(PAYLOAD)
    payload['document'] = recipe
    response = session.post(action, json=payload)
    return response


def insert_many(recipes: List[Dict[str, Any]]) -> 'requests.Response':
    """Insert many recipes into the database.

    Args:
        recipes (List[Dict[str, Any]]): Recipes to insert.

    Returns:
        requests.Response: Response from the API.
    """
    session = create_session()
    action = f'{END_POINT}/insertMany'
    payload: Dict[str, Any] = copy.deepcopy(PAYLOAD)
    payload['documents'] = recipes
    response = session.post(action, json=payload)
    return response


def find_one(query: Dict[str, Any]) -> Any:
    session = create_session()
    action = f'{END_POINT}/findOne'
    payload: Dict[str, Any] = copy.deepcopy(PAYLOAD)
    payload['filter'] = query
    response = session.post(action, json=payload)
    return response.json()
