from django.urls import path

from recipes import views

urlpatterns = [
    path('author/<int:author_id>/', views.get_author_recipes,
         name='author_recipes'),
    path('<int:recipe_id>/', views.get_recipe, name='recipe'),
    path('<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('followings/', views.get_followings, name='followings'),
    path('new/', views.create_recipe, name='new_recipe'),
    path('favorites/', views.get_favorites, name='favorites'),
    path('shop_list/', views.get_shop_list, name='shop_list'),
    path('pdf_shop_list/', views.get_pdf_shop_list, name='pdf_shop_list')
]
