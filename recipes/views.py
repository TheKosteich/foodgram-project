from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from recipes.models import Recipe, Follow


def get_recipes(request):
    recipes = Recipe.objects.select_related('author',).order_by('title')
    context = {'paginator': Paginator(recipes, 9)}
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
    return render(request, 'recipes/shop_list.html')


def get_favorites(request):
    return render(request, 'recipes/favorites.html')


# service functions described below
def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
