import os
import random
import string
from datetime import datetime as dt

from fpdf import FPDF

from foodgram.settings import DOWNLOADS_DIR
from recipes.models import Ingredient
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


def get_request_tags(request_dict):
    existing_tags = Tag.objects.all()
    tag_names = [tag.name for tag in existing_tags]
    request_tags = []
    for key, value in request_dict.items():
        if key in tag_names and value == 'on':
            request_tags.append(key)
    return request_tags
