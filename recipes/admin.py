from django.contrib import admin

from recipes.models import Ingredient


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    pass
    # list_display = ('title', 'dimension')
