from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import IngredientSerializer
from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeToShopping)

User = get_user_model()


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class FollowingsAPIView(APIView):
    def post(self, request):
        user = request.user
        if 'id' in request.data:
            following = get_object_or_404(User, id=request.data['id'])
            if user.followings.filter(following=following).exists():
                return Response({'success': 'False'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': 'False'},
                            status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(user=user, following=following)
        return Response({'success': 'True'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        following = User.objects.get(id=request.data['id'])
        is_follow = user.followings.filter(following=following).exists()
        if is_follow:
            user.followings.filter(following=following).delete()
            return Response({'success': 'True'}, status=status.HTTP_200_OK)
        return Response({'success': 'False'},
                        status=status.HTTP_400_BAD_REQUEST)


class RecipesToShoppingAPIView(APIView):
    def post(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        is_in_shopping_list = RecipeToShopping.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
        if is_in_shopping_list:
            return Response({'success': 'False'},
                            status=status.HTTP_400_BAD_REQUEST)
        RecipeToShopping.objects.create(user=request.user, recipe=recipe)
        return Response({'success': 'True'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        is_in_shopping_card = RecipeToShopping.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
        if is_in_shopping_card:
            RecipeToShopping.objects.filter(user=request.user,
                                            recipe=recipe).delete()
            return Response({'success': 'True'}, status=status.HTTP_200_OK)
        return Response({'success': 'False'},
                        status=status.HTTP_400_BAD_REQUEST)


class FavoritesAPIView(APIView):
    def post(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        user = request.user
        is_favorite = user.favorites.filter(recipe_id=recipe.id).exists()
        if is_favorite:
            return Response({'success': 'False'},
                            status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=user, recipe=recipe)
        return Response({'success': 'True'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        user = request.user
        is_favorite = user.favorites.filter(recipe_id=recipe.id).exists()
        if is_favorite:
            user.favorites.get(recipe_id=recipe.id).delete()
            return Response({'success': 'True'}, status=status.HTTP_200_OK)
        return Response({'success': 'False'},
                        status=status.HTTP_400_BAD_REQUEST)
