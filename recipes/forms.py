from django import forms

from recipes.models import Recipe


class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time', 'description', 'image']
        labels = {
            'title': 'Название рецепта',
            'cooking_time': 'Время приготовления',
            'description': 'Описание',
            'image': 'Загрузить фото'
        }
