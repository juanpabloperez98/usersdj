from django.urls import path
from .views import *

app_name = "users_app"

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('update/', UpdatePassword.as_view(), name="user-update"),
    path('user-verification/<pk>', CodeVerificationView.as_view(), name="user-verification"),
]