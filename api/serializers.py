from rest_framework import serializers
from django.contrib.auth import get_user_model

from recipes.models import (
    Ingredient, Recipe, RecipeIngredients, Favorite, Follow, UserPurchases
)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']


class FollowSerializer(serializers.ModelSerializer):
    pass


class UserPurchasesSerializer(serializers.ModelSerializer):
    pass


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe', )
