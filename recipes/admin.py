from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredients


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
