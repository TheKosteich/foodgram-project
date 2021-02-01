from django.contrib import admin

from recipes.models import Favorite
from recipes.models import Follow
from recipes.models import Ingredient
from recipes.models import Recipe
from recipes.models import RecipeIngredients
from recipes.models import RecipesToShopping


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    ordering = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientsInline,)


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipesToShopping)
class UserRecipesAdmin(admin.ModelAdmin):
    pass
