from django.urls import path
from recipes import views


urlpatterns = [
    path('follows/', views.get_follows, name='follows'),
    path('create/', views.create_recipe, name='new_recipe')
]
