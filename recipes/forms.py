from django import forms

from recipes.models import Recipe


class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'ingredients',
                  'cooking_time', 'description', 'image']
        # labels = {
        #     'text': 'Текст',
        #     'group': 'Группа',
        #     'image': 'Изображение'
        # }
