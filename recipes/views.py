from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import PAGE_ITEMS_COUNT
from recipes.forms import NewRecipeForm
from recipes.models import Recipe, RecipeIngredient, Ingredient
from recipes.utils import (get_request_ingredients, get_request_form_tags,
                           get_tagged_recipes)

User = get_user_model()


def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipes/recipe_card.html', context=context)


def get_recipes(request):
    context = {}
    context['tags'], recipes = get_tagged_recipes(request)
    context['paginator'] = Paginator(recipes, PAGE_ITEMS_COUNT)
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/recipes.html', context=context)


def get_author_recipes(request, author_id):
    author = get_object_or_404(User, id=author_id)
    context = {'author': author}
    context['tags'], recipes = get_tagged_recipes(request, author=author)
    context['paginator'] = Paginator(recipes, PAGE_ITEMS_COUNT)
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/recipes.html', context=context)


@login_required(login_url='login')
def get_followings(request):
    context = {'followings': request.user.followings.all()}
    return render(request, 'recipes/followings.html', context=context)


@login_required(login_url='login')
def create_recipe(request):
    new_recipe_form = NewRecipeForm(request.POST or None,
                                    request.FILES or None)
    if new_recipe_form.is_valid():
        new_recipe = Recipe.objects.create(
            author=request.user,
            **new_recipe_form.cleaned_data
        )
        for tag in get_request_form_tags(request.POST):
            new_recipe.tags.add(tag)
        for key, value in get_request_ingredients(request.POST).items():
            RecipeIngredient.objects.create(
                recipe=new_recipe,
                ingredient=key,
                amount=value
            )
        return redirect(new_recipe)
    context = {'form': new_recipe_form}
    return render(request, 'recipes/new_recipe.html', context=context)


@login_required(login_url='login')
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe_form = NewRecipeForm(request.POST or None,
                                request.FILES or None,
                                instance=recipe)
    if recipe_form.is_valid():
        recipe_form.save()
        recipe.tags.clear()
        for tag in get_request_form_tags(request.POST):
            recipe.tags.add(tag)
        recipe.recipe_ingredients.all().delete()
        for key, value in get_request_ingredients(request.POST).items():
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=key,
                amount=value
            )
        return redirect(recipe)

    context = {
        'edit_recipe': True,
        'recipe': recipe,
        'form': recipe_form,
        'tags': list(recipe.tags.values_list('name', flat=True)),
        'recipe_ingredients': recipe.recipe_ingredients.all()
    }

    return render(request, 'recipes/new_recipe.html', context=context)


@login_required(login_url='login')
def get_shop_list(request):
    context = {
        'shop_list': request.user.recipes_to_shopping.all()
    }
    return render(request, 'recipes/shop_list.html', context=context)


@login_required(login_url='login')
def get_pdf_shop_list(request):
    recipes_to_shopping = request.user.recipes_to_shopping.all()
    user_purchases = {}

    for item in recipes_to_shopping:
        recipe = item.recipe
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        for recipe_ingredient_item in recipe_ingredients:
            ingredient_title = recipe_ingredient_item.ingredient.title
            ingredient_amount = recipe_ingredient_item.amount
            if ingredient_title in user_purchases.keys():
                user_purchases[ingredient_title] += ingredient_amount
            else:
                user_purchases[ingredient_title] = ingredient_amount

    content = ''

    for purchase, amount in user_purchases.items():
        dimension = Ingredient.objects.get(title=purchase).dimension
        content += f'( ) {purchase} - {amount} {dimension}\n'

    filename = 'shop_list.txt'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response


@login_required(login_url='login')
def get_favorites(request):
    context = {}
    favorites = request.user.favorites.all()
    context['tags'], recipes = get_tagged_recipes(request,
                                                  favorites=favorites)
    context['paginator'] = Paginator(recipes, PAGE_ITEMS_COUNT)
    page_number = request.GET.get('page')
    context['page'] = context['paginator'].get_page(page_number)
    return render(request, 'recipes/favorites.html', context=context)
