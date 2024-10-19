from django.contrib import admin
from .models import Conversation


# Register your models here.
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "title",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "owner",
        "created_at",
        "updated_at",
    )
