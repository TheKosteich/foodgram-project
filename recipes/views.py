from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import mimetypes

from recipes.models import Recipe
from recipes.models import Follow
from recipes.models import Favorite
from recipes.models import UserPurchases
from recipes.models import RecipesToShopping
from recipes.models import RecipeIngredients
from recipes.forms import NewRecipeForm
from taggit.models import Tag

from recipes.utils import get_shop_list_pdf
from recipes.utils import get_request_ingredients
from recipes.utils import get_request_tags

User = get_user_model()


def get_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipes/recipe_card.html', context=context)


def get_recipes(request):
    context = {}
    if 'tags' in request.GET.keys():
        tags_names = request.GET['tags'].lower().split(',')
        recipes = Recipe.objects.filter(
            tags__name__in=tags_names
        ).distinct().order_by('title')
    else:
        tags = Tag.objects.all()
        tags_names = [tag.name for tag in tags]
        recipes = Recipe.objects.select_related('author', ).order_by('title')
    context['tags'] = tags_names
    context['paginator'] = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/recipes.html', context=context)


def get_author_recipes(request, author_id):
    author = get_object_or_404(User, id=author_id)
    context = {'author': author}
    if 'tags' in request.GET.keys():
        tags_names = request.GET['tags'].lower().split(',')
        recipes = Recipe.objects.filter(
            author=author,
            tags__name__in=tags_names
        ).distinct().order_by('title')
    else:
        tags = Tag.objects.all()
        tags_names = [tag.name for tag in tags]
        recipes = Recipe.objects.filter(author=author).order_by('title')
    context['tags'] = tags_names
    context['paginator'] = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/recipes.html', context=context)


@login_required(login_url='login')
def get_followings(request):
    context = {'followings': request.user.followings.all()}
    return render(request, 'recipes/followings.html', context=context)


@login_required(login_url='login')
def create_recipe(request):
    context = {}
    if request.method == 'POST':
        new_recipe_form = NewRecipeForm(request.POST or None,
                                        request.FILES or None)
        if new_recipe_form.is_valid():
            new_recipe = Recipe.objects.create(
                author=request.user,
                **new_recipe_form.cleaned_data
            )
            for tag in get_request_tags(request.POST):
                new_recipe.tags.add(tag)
            for key, value in get_request_ingredients(request.POST).items():
                RecipeIngredients.objects.create(
                    recipe=new_recipe,
                    ingredient=key,
                    amount=value
                )
            return redirect(new_recipe)
    elif request.method == 'GET':
        context = {'form': NewRecipeForm()}
    return render(request, 'recipes/new_recipe.html', context=context)


@login_required(login_url='login')
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'GET':
        data = {
            'title': recipe.title,
            'cooking_time': recipe.cooking_time,
            'description': recipe.description,
            'image': recipe.image
        }
        recipe_form = NewRecipeForm(initial=data)
        context = {
            'edit_recipe': True,
            'recipe': recipe,
            'form': recipe_form,
            'tags': [tag.name for tag in recipe.tags.all()],
            'recipe_ingredients': recipe.recipe_ingredients.all()
        }

        return render(request, 'recipes/new_recipe.html',
                      context=context)
    elif request.method == 'POST':
        print('POST')
        recipe_form = NewRecipeForm(request.POST or None,
                                    request.FILES or None,
                                    instance=recipe)
        if recipe_form.is_valid():
            recipe_form.save()
            recipe.tags.clear()
            for tag in get_request_tags(request.POST):
                recipe.tags.add(tag)
            recipe.recipe_ingredients.all().delete()
            for key, value in get_request_ingredients(request.POST).items():
                RecipeIngredients.objects.get_or_create(
                    recipe=recipe,
                    ingredient=key,
                    amount=value
                )
    return redirect(recipe)


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
    context = {'paginator': Paginator(recipes, 3)}
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/favorites.html', context=context)


# service functions described below
def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
