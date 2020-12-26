from rest_framework.routers import DefaultRouter
from django.urls import path, include

from  api.views import IngredientsViewSet

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('v1', include(router_v1.urls)),
]
