from django.urls import path
from . import views

urlpatterns = [
    path("", views.GetConversations.as_view()),
]
