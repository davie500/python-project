from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "updated_at", "created_at")
    list_filter = ("updated_at", "created_at")
    search_fields = ("title", "user__username", "user__email")
    ordering = ("-updated_at", "-created_at")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "role", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("content", "conversation__title", "conversation__user__username")
    ordering = ("-created_at",)

