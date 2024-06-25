# auth_app/urls.py
from django.urls import path
from .views import LoginView, RegisterView, ChangePasswordView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
]

