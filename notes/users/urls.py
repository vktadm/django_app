"""Определяет схемы URL для users."""

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # Страница авторизации.
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('', include('django.contrib.auth.urls')),
    # Страница регистрации.
    path('register/', views.register, name='register'),
]