""" This file contains the forms for the application. """

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, \
    validators, TextAreaField, URLField


class RecipeEditForm(FlaskForm):  # type: ignore
    """Recipe editor form for the application.
    Args:
        Form (_type_): WTForms class.
    """
    name = StringField('name', [validators.Length(min=4, max=25)])
    image = URLField('image', [validators.URL()])
    ingredients = StringField('ingredients', [validators.InputRequired()])
    prep_time = IntegerField('prep_time', [validators.InputRequired()])
    cook_time = IntegerField('cook_time', [validators.InputRequired()])
    steps = TextAreaField('instructions', [validators.InputRequired()])
