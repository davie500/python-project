from django.urls import path

from . import views

app_name = "chat"


urlpatterns = [
    path("", views.conversation_list, name="conversation_list"),
    path("new/", views.conversation_create, name="conversation_create"),
    path(
        "<int:conversation_id>/",
        views.conversation_detail,
        name="conversation_detail",
    ),
    path(
        "<int:conversation_id>/send/",
        views.message_create,
        name="message_create",
    ),
]

