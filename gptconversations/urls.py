from django.urls import path
from . import views

urlpatterns = [
    path("", views.ConversationsList.as_view()),
    path("<int:id>/", views.ConversationMessages.as_view()),
]
