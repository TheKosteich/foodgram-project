from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import IngredientsViewSet
from api.views import FavoriteViewSet
from api.views import FavoritesAPIView
from api.views import FollowViewSet


router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
# router_v1.register('favorites', FavoriteViewSet, basename='favorites')
# router_v1.register('favorites', FavoritesAPIView, basename='favorites')
router_v1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/favorites/<int:recipe_id>/', FavoritesAPIView.as_view(),
         name='favorites'),
]
