from django.urls import path

from users import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<str:username>/', views.get_profile, name='profile'),
]
