from django.urls import path
from . import views

urlpatterns = [
    path("", views.ai_assistant, name="ai_assistant"),
    path("new/", views.new_conversation, name="new_ai_conversation"),
    path(
        "conversation/<int:conversation_id>/",
        views.ai_assistant,
        name="ai_conversation",
    ),
    path(
        "conversation/<int:conversation_id>/delete/",
        views.delete_conversation,
        name="delete_ai_conversation",
    ),
    path(
        "client/",
        views.client_ai,
        name="client_ai"
    ),
     path(
        "client/new/",
        views.client_new_conversation,
        name="client_new_ai_conversation"
    ),
    path(
        "client/conversation/<int:conversation_id>/",
        views.client_ai,
        name="client_ai_conversation"
    ),
]