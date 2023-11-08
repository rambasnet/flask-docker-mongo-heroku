"""
This is the main file of the Flask application.
"""

from typing import Any
import os
from flask import Flask, render_template
import db_api
from flask import request
import forms

app = Flask(__name__)


@app.route('/')
def home() -> Any:
    """Home page of the application.

    Returns:
        str: HTML page using Jinja2 template.
    """
    context = {
        'title': 'Flask App with Bootstrap5 Template',
        'content': 'Some content you can read from database...'
    }
    return render_template('home.html', **context)


@app.route('/recipes')
def show_all_recipes() -> Any:
    """Recipes page of the application.

    Returns:
        str: HTML page using Jinja2 template.
    """
    documents = db_api.find_all({})

    context = {
        'title': 'Spanish Recipes',
        'recipes': documents['documents']
    }
    return render_template('recipes.html', **context)


@app.route('/recipe/<string:recipe_id>')
def single_recipe(recipe_id: str) -> Any:
    """Recipe page of the application.

    Args:
        recipe_id (str): Recipe id.

    Returns:
        str: HTML page using Jinja2 template.
    """
    context = {
        'title': 'Spanish Recipes',
        'recipe': None
    }
    if recipe_id != '...':  # this is a bizzare workaround!
        # Not sure why it makes GET /recipe/... request automatically
        doc = db_api.find_one({'_id': {"$oid": recipe_id}})
        # print(f'{doc=}')
        recipe = doc['document']
        context['recipe'] = recipe

    return render_template('recipe.html', **context)


@app.route('/update/<string:recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id: str) -> Any:
    """Update recipe page of the application.

    Args:
        recipe_id (str): Recipe id.

    Returns:
        str: HTML page using Jinja2 template.
    """
    form = forms.RecipeEditForm(request.form)
    # print('form', form)
    where = {'_id': {"$oid": recipe_id}}
    recipe = db_api.find_one(where)['document']
    context = {
        'error': "",
        'success': "",
        'title': 'Spanish Recipes',
        'recipe': recipe,
        'form': form}
    if request.method == 'POST' and form.validate():
        ingredients = form.ingredients.data.strip().split(',')
        update = {
            '$set': {
                'name': form.name.data.strip(),
                'image': form.image.data.strip(),
                'ingredients': ingredients,
                'prep_time': form.prep_time.data,
                'cook_time': form.cook_time.data,
                'steps': form.steps.data.strip()
            }
        }
        # print(f'{update=}')
        result = db_api.update_one(where, update)
        if result['modifiedCount'] == 1:
            success = f"Recipe {recipe['name']} updated successfully"
            context['success'] = success
            recipe = db_api.find_one(where)['document']
            recipe['ingredients'] = ', '.join(recipe.get('ingredients', []))
            context['recipe'] = recipe
            # print(recipe)
    else:
        context['error'] = form.errors
        recipe['ingredients'] = ', '.join(recipe.get('ingredients', []))
    # print('errors', form.errors)
    # print('validate', form.validate())
    return render_template('update.html', **context)


@app.route('/delete/<string:recipe_id>')
def delete_recipe(recipe_id: str) -> Any:
    """Delete recipe page of the application.

    Args:
        recipe_id (str): Recipe id.

    Returns:
        str: HTML page using Jinja2 template.
    """

    result = db_api.delete_one({'_id': {"$oid": recipe_id}})
    if result['deletedCount'] == 1:
        message = f"Recipe {recipe_id} deleted successfully"
    context = {'message': message, 'title': 'Spanish Recipes'}
    return render_template('message.html', **context)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
