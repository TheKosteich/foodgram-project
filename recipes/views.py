from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
import mimetypes

from recipes.models import Recipe
from recipes.models import Follow
from recipes.models import Favorite
from recipes.models import UserPurchases
from recipes.models import RecipesToShopping
from recipes.models import RecipeIngredients

from recipes.utils import get_shop_list_pdf


def get_recipes(request):
    if 'tags' in request.GET.keys():
        tags = request.GET['tags'].lower().split(',')
        recipes = Recipe.objects.filter(tags__name__in=tags).order_by('title')
    else:
        recipes = Recipe.objects.select_related('author', ).order_by('title')
    context = {'paginator': Paginator(recipes, 2)}
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/recipes.html', context=context)


@login_required(login_url='login')
def get_followings(request):
    context = {'followings': request.user.followings.all()}
    return render(request, 'recipes/followings.html', context=context)


@login_required(login_url='login')
def create_recipe(request):
    return render(request, 'recipes/new_recipe.html')


def get_shop_list(request):
    context = {
        'shop_list': request.user.recipes_to_shopping.all()
    }
    return render(request, 'recipes/shop_list.html', context=context)


def get_pdf_shop_list(request):
    recipes_to_shopping = request.user.recipes_to_shopping.all()
    user_purchases = {}

    for item in recipes_to_shopping:
        recipe = item.recipe
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        for recipe_ingredient_item in recipe_ingredients:
            ingredient_title = recipe_ingredient_item.ingredient.title
            ingredient_amount = recipe_ingredient_item.amount
            if ingredient_title in user_purchases.keys():
                user_purchases[ingredient_title] += ingredient_amount
            else:
                user_purchases[ingredient_title] = ingredient_amount

    pdf_shop_list_path = get_shop_list_pdf(user_purchases)

    pdf_shop_list = open(pdf_shop_list_path, 'rb')

    return FileResponse(pdf_shop_list)


def get_favorites(request):
    favorites = request.user.favorites.all()
    recipes = Recipe.objects.filter(
        id__in=favorites.values_list('recipe', flat=True)
    ).order_by('title')
    context = {'paginator': Paginator(recipes, 9)}
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/favorites.html', context=context)


# service functions described below
def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
