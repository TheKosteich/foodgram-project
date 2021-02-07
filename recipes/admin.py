from django.contrib import admin

from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, RecipeToShopping)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    ordering = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientsInline,)


@admin.register(RecipeIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeToShopping)
class UserRecipesAdmin(admin.ModelAdmin):
    pass
