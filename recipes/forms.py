from django import forms

from recipes.models import Recipe
from recipes.utils import get_request_ingredients


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

    def clean(self):
        cleaned_data = super().clean()
        recipe_ingredients = get_request_ingredients(self.data)
        if recipe_ingredients:
            for key, value in get_request_ingredients(self.data).items():
                if int(value) < 1:
                    raise forms.ValidationError(
                        'Возможно только положительное колличество'
                        ' ингредиентов',
                        code='ingredients'
                    )
        else:
            raise forms.ValidationError(
                'Необходимо добавить хотябы один ингредиент',
                code='ingredients'
            )
        return cleaned_data
