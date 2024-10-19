from django.urls import path
from . import views

urlpatterns = [
    path("", views.GetMessages.as_view()),
]
