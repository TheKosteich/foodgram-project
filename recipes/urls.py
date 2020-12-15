from django.urls import path
from recipes import views


urlpatterns = [
    path('follows/', views.get_follows, name='follows'),
    path('new/', views.create_recipe, name='new_recipe'),
    path('favorites/', views.get_favorites, name='favorites'),
    path('shop_list/', views.get_shop_list, name='shop_list'),
]
