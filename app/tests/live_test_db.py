"""
Test module for unit testing db_api.py
"""

from typing import Dict, Any
import sys
import unittest
import os

from app.db_api import insert_one
from app.db_api import insert_many
from app.db_api import find_one

# add the parent directory to the path
current_dir = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current_dir)
sys.path.append(parent)
# print(sys.path, file=sys.stderr)


def spanish_omelet() -> Dict[str, Any]:
    return {
        'name': 'Spanish Omelet',
        'ingredients': [
            'egg',
            'potato',
            'onion',
            'olive oil',
            'salt'
        ],
        'steps': [
            'Peel and slice the potatoes into thin round pieces.',
            'Peel and slice the onion into thin pieces.',
            'Heat the olive oil in a pan.',
            'Add the potatoes and onion to the pan and \
                cook for 20 minutes on medium heat.',
            'Beat the eggs in a large bowl and add salt.',
            'Add the cooked potatoes and onion to the bowl and mix well.',
            'Heat a pan with a little olive oil and add the mixture.',
            'Cook for 5 minutes on one side and then flip it \
                over and cook for another 5 minutes.'
        ],
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/\
            Tortilla_de_patata_-_San_Sebasti%C3%A1n.jpg/\
                440px-Tortilla_de_patata_-_San_Sebasti%C3%A1n.jpg',
        'prep_time': 30,
        'cook_time': 20,
        'servings': 4,
        'tags': [
            'spanish',
            'omelet',
            'potato',
            'egg',
            'onion'
        ]
    }


class Test_DB_API(unittest.TestCase):
    def test_insert_one(self) -> None:
        """Test insert_one function.
        """
        recipe = spanish_omelet()
        response = insert_one(recipe)
        print(f'{response=}', file=sys.stderr)
        # 201 means the document was created
        assert response.status_code == 201
        json_response = response.json()
        print(json_response, file=sys.stderr)
        assert json_response['insertedId'] is not None

    def test_insert_one_1(self) -> None:
        """Test insert_one function.
        """
        recipe = {
            "name": "Beef Enchilada",
            "ingredients": [
                "potato",
                "onion",
                "ground beef",
                "oil",
                "tortillas",
                "cheese"
            ],
            "prep_time": 35
        }
        response = insert_one(recipe)
        assert response.status_code == 201
        json_response = response.json()
        assert json_response['insertedId'] is not None

    def test_insert_many(self) -> None:
        """Test insert_many function.
        """
        response = insert_many([spanish_omelet(), spanish_omelet()])
        print('REESPONSE', response, file=sys.stderr)
        json_response = response.json()
        assert response.status_code == 201
        assert json_response['insertedIds'] is not None
        assert len(json_response['insertedIds']) == 2

    def test_find_one(self) -> None:
        """Test find_one function.
        """
        response = find_one({'name': 'Spanish Omelet'})
        print(response, file=sys.stderr)
        document = response['document']
        omelet = spanish_omelet()
        assert document['name'] == 'Spanish Omelet'
        assert document['ingredients'] == omelet['ingredients']
        assert document['steps'] == omelet['steps']
        assert document['image'] == omelet['image']
        assert document['prep_time'] == omelet['prep_time']
        assert document['cook_time'] == omelet['cook_time']
        assert document['servings'] == omelet['servings']
        assert document['tags'] == omelet['tags']


if __name__ == '__main__':
    unittest.main(verbosity=2)
