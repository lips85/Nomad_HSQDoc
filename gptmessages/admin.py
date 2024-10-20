from django.contrib import admin
from .models import Message


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "conversation",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "conversation",
        "created_at",
        "updated_at",
    )
