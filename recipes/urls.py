from django.urls import path
from recipes import views


urlpatterns = [
    path('followings/', views.get_followings, name='followings'),
    path('new/', views.create_recipe, name='new_recipe'),
    path('favorites/', views.get_favorites, name='favorites'),
    path('shop_list/', views.get_shop_list, name='shop_list'),
]
