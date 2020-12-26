from rest_framework import serializers
from django.contrib.auth import get_user_model

from recipes.models import (
    Ingredient, Recipe, RecipeIngredients, Favorite, Follow
)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']


class FavoriteSerializer(serializers.ModelSerializer):
    pass


class FollowSerializer(serializers.ModelSerializer):
    pass
