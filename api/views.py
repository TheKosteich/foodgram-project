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
from api.serializers import FavoriteSerializer
from api.serializers import FollowSerializer
from recipes.models import Ingredient
from recipes.models import Recipe
from recipes.models import Follow
from recipes.models import UserPurchases
from recipes.models import Favorite


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


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        favorites = get_list_or_404(
            Favorite,
            user=self.request.user
        )
        return favorites

    def get_object(self):
        recipe_id = self.kwargs.get(self.lookup_field)
        favorite = get_object_or_404(
            Favorite,
            user=self.request.user,
            recipe_id=recipe_id
        )
        return favorite


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
        return Response(
            {'success': 'False'}, status=status.HTTP_400_BAD_REQUEST
        )
