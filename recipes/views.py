from django.core.paginator import Paginator
from django.shortcuts import render

from recipes.models import Recipe


def get_recipes(request):
    recipes = Recipe.objects.all()
    context = {'paginator': Paginator(recipes, 9)}
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/recipes.html', context=context)


def get_follows(request):
    return render(request, 'recipes/follows.html')


def create_recipe(request):
    return render(request, 'recipes/new_recipe.html')


def get_shop_list(request):
    return render(request, 'recipes/shop_list.html')


def get_favorites(request):
    return render(request, 'recipes/favorites.html')


# service functions described below
def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
