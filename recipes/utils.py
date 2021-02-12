import random
import string

from taggit.models import Tag

from recipes.models import Ingredient, Recipe


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


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
        if author is not None:
            recipes = Recipe.objects.filter(
                author=author,
                tags__name__in=tags_names
            ).distinct().order_by('title')
        elif favorites is not None:
            recipes = Recipe.objects.filter(
                tags__name__in=tags_names,
                id__in=favorites.values_list('recipe', flat=True)
            ).distinct().order_by('title')
        else:
            recipes = Recipe.objects.filter(
                tags__name__in=tags_names
            ).distinct().order_by('title')
    else:
        tags_names = list(Tag.objects.values_list('name', flat=True))
        if author is not None:
            recipes = Recipe.objects.filter(author=author).order_by('title')
        elif favorites is not None:
            recipes = Recipe.objects.filter(
                id__in=favorites.values_list('recipe', flat=True)
            ).order_by('title')
        else:
            recipes = Recipe.objects.select_related('author', ).order_by(
                'title')

    return tags_names, recipes
