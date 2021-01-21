from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from api.serializers import IngredientSerializer
from api.serializers import FollowSerializer
from recipes.models import Ingredient
from recipes.models import Recipe
from recipes.models import Follow
from recipes.models import UserPurchases
from recipes.models import Favorite
from recipes.models import RecipesToShopping


User = get_user_model()


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class UserPurchasesViewSet(viewsets.ModelViewSet):
    pass


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']


class RecipesToShoppingAPIView(APIView):
    def post(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        is_in_shopping_list = RecipesToShopping.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
        if is_in_shopping_list:
            return Response({'success': 'False'},
                            status=status.HTTP_400_BAD_REQUEST)
        RecipesToShopping.objects.create(user=request.user, recipe=recipe)
        return Response({'success': 'True'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        is_in_shopping_card = RecipesToShopping.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
        if is_in_shopping_card:
            RecipesToShopping.objects.filter(user=request.user,
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
