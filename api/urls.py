from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (FavoritesAPIView, FollowingsAPIView,
                       IngredientsViewSet, RecipesToShoppingAPIView)

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('v1/', include([
        path('', include(router_v1.urls)),
        path('favorites/', FavoritesAPIView.as_view(), name='favorites'),
        path('followings/', FollowingsAPIView.as_view(), name='followings'),
        path('purchases/', RecipesToShoppingAPIView.as_view(),
             name='purchases'),
    ])),
]
