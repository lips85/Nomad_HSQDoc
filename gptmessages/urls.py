from django.urls import path
from . import views

urlpatterns = [
    path("", views.MessagesLists.as_view()),
    path("<int:id>/", views.ConversationMessages.as_view()),
]
