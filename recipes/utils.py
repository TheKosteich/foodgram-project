import os
import random
import string
from datetime import datetime as dt

from fpdf import FPDF

from foodgram.settings import DOWNLOADS_DIR
from recipes.models import Ingredient, Recipe
from taggit.models import Tag


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_shop_list_pdf(user_purchases):
    """Function input parameter - user_purchases is dict.
    Return full path pdf shop list document."""
    pdf_shop_list = FPDF()
    pdf_shop_list.add_page()

    font_path = os.path.join(
        os.getcwd(),
        'recipes/static/recipes/fonts/DejaVuSansCondensed.ttf'
    )
    pdf_shop_list.add_font(family='DejaVu', fname=font_path, uni=True)
    pdf_shop_list.set_font(family='DejaVu', size=14)

    for purchase, amount in user_purchases.items():
        pdf_shop_list.cell(0, 10, f'( ) {purchase} - {amount}', 0, 1)

    date, random_string = dt.now().date(), get_random_string(8)
    shop_list_name = f'{date}_shop-list_{random_string}.pdf'
    shop_list_full_path = os.path.join(DOWNLOADS_DIR, shop_list_name)
    pdf_shop_list.output(name=shop_list_full_path)

    return shop_list_full_path


def get_request_ingredients(request_dict):
    """Input parameter - request parameters dictionary.
    Function make recipe ingredients dictionary and return it."""
    recipe_ingredients = {}
    for key, value in request_dict.items():
        if 'nameIngredient' in key:
            ingredient_post_index = key[key.index('_') + 1:]
            dimension = request_dict[
                f'unitsIngredient_{ingredient_post_index}'
            ]
            ingredient, created = Ingredient.objects.get_or_create(
                title=value,
                dimension=dimension
            )

            recipe_ingredients[ingredient] = request_dict[
                f'valueIngredient_{ingredient_post_index}'
            ]
    return recipe_ingredients


def get_request_form_tags(request_dict):
    """Input parameter - request parameters dictionary.
    Function make tags list from request form parameters and return it."""
    tag_names = Tag.objects.values_list('name', flat=True)
    request_tags = []
    for key, value in request_dict.items():
        if key in tag_names and value == 'on':
            request_tags.append(key)
    return request_tags


def get_tagged_recipes(request, author=None, favorites=None):
    """Input parameter - request parameters dictionary and author object.
    Function make tags list from request get parameters and select tagged
    recipes from db.
    Return tags names and tagged recipes."""
    if 'tags' in request.GET.keys():
        tags_names = request.GET['tags'].lower().split(',')
        if author:
            recipes = Recipe.objects.filter(
                author=author,
                tags__name__in=tags_names
            ).distinct().order_by('title')
        elif favorites:
            recipes = Recipe.objects.filter(
                tags__name__in=tags_names,
                id__in=favorites.values_list('recipe', flat=True)
            ).order_by('title')
        else:
            recipes = Recipe.objects.filter(
                tags__name__in=tags_names
            ).distinct().order_by('title')
    else:
        tags_names = list(Tag.objects.values_list('name', flat=True))
        if author:
            recipes = Recipe.objects.filter(author=author).order_by('title')
        elif favorites:
            recipes = Recipe.objects.filter(
                id__in=favorites.values_list('recipe', flat=True)
            ).order_by('title')
        else:
            recipes = Recipe.objects.select_related('author', ).order_by(
                'title')

    return tags_names, recipes
