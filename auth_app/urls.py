# auth_app/urls.py
from django.urls import path
from .views import LoginView, RegisterView, ChangePasswordView, ChangePasswordByIdView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('change-password/<str:user_id>', ChangePasswordByIdView.as_view(), name='change_password_by_id'),
]

