from django.contrib import admin
from .models import Conversation


# Register your models here.
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "title",
        "file_name",
        "file_url",
    )
    list_filter = (
        "owner",
        "file_name",
        "created_at",
        "updated_at",
    )
