from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404

from recipes.models import Recipe
from recipes.models import Follow
from recipes.models import Favorite
from recipes.models import UserPurchases
from recipes.models import RecipesToShopping


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
    context = {
        'shop_list': request.user.recipes_to_shopping.all()
    }
    return render(request, 'recipes/shop_list.html', context=context)


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
