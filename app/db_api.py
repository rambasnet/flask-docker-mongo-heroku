"""
MongoDB database APIs.
"""
import copy
from typing import Dict, List, Any
import requests
import settings


def create_session() -> requests.Session:
    """Create a session with the API header.

    Returns:
        requests.Session: Session with the API header.
    """
    session = requests.Session()
    session.headers.update(settings.HEADERS)
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
    action = f'{settings.END_POINT}/insertOne'
    print(action)
    payload: Dict[str, Any] = copy.deepcopy(settings.PAYLOAD)
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
    action = f'{settings.END_POINT}/insertMany'
    payload: Dict[str, Any] = copy.deepcopy(settings.PAYLOAD)
    payload['documents'] = recipes
    response = session.post(action, json=payload)
    return response


def find_one(query: Dict[str, Any]) -> Any:
    """Find one recipe.

    Args:
        query (Dict[str, Any]): filter for find_one API.

    Returns:
        Any: Recipe.
    """
    session = create_session()
    action = f'{settings.END_POINT}/findOne'
    payload: Dict[str, Any] = copy.deepcopy(settings.PAYLOAD)
    payload['filter'] = query
    response = session.post(action, json=payload)
    return response.json()


def find_all(query: Dict[str, Any]) -> Any:
    """Find all recipes.

    Args:
        query (Dict[str, Any]): filter for find_all API.

    Returns:
        Any: Recipes.
    """
    session = create_session()
    action = f'{settings.END_POINT}/find'
    payload: Dict[str, Any] = copy.deepcopy(settings.PAYLOAD)
    payload['filter'] = query
    response = session.post(action, json=payload)
    return response.json()


def delete_one(query: Dict[str, Any]) -> Any:
    """Delete one recipe.

    Args:
        query (Dict[str, Any]): filter for delete_one API.

    Returns:
        Any: Response from the API.
    """
    session = create_session()
    action = f'{settings.END_POINT}/deleteOne'
    payload: Dict[str, Any] = copy.deepcopy(settings.PAYLOAD)
    payload['filter'] = query
    response = session.post(action, json=payload)
    return response.json()


def update_one(query: Dict[str, Any], update: Dict[str, Any]) -> Any:
    """Update one recipe.

    Args:
        query (Dict[str, Any]): filter for update_one API.
        update (Dict[str, Any]): update for update_one API.

    Returns:
        Any: Response from the API.
    """
    session = create_session()
    action = f'{settings.END_POINT}/updateOne'
    payload: Dict[str, Any] = copy.deepcopy(settings.PAYLOAD)
    payload['filter'] = query
    payload['update'] = update
    response = session.post(action, json=payload)
    return response.json()
