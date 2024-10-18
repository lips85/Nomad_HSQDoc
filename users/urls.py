from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.UserRegister.as_view()),
    path("profile/", views.UserProfile.as_view()),
    path("profile/password/", views.ChangePassword.as_view()),
    path("login/", views.JWTLogIn.as_view()),
    path("logout/", views.LogOut.as_view()),
]
