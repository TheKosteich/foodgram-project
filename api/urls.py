from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import IngredientsViewSet
from api.views import FavoritesAPIView
from api.views import RecipesToShoppingAPIView
from api.views import FollowingsAPIView


router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/favorites/', FavoritesAPIView.as_view(), name='favorites'),
    path('v1/followings/', FollowingsAPIView.as_view(), name='followings'),
    path('v1/purchases/', RecipesToShoppingAPIView.as_view(),
         name='purchases'),
]
