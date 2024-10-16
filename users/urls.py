from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("<int:pk>/", views.UserView.as_view()),
    path("password/", views.ChangePassword.as_view()),
    path("login/", views.JWTLogIn.as_view()),
    path("logout/", views.LogOut.as_view()),
]
