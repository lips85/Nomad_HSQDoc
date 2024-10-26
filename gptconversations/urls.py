from django.urls import path
from . import views

urlpatterns = [
    path("", views.ConversationsList.as_view()),
    path("<int:id>/", views.ConversationDetail.as_view()),
    path("<int:id>/usage/", views.ConversationUsage.as_view()),
]
