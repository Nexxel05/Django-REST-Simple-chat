from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin

from core.models import User, Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("created", "updated")


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = (
        "sender",
        "text",
        "thread",
        "created",
        "is_read"
    )
    search_fields = ("text",)
    list_filter = ("sender", "is_read")


@admin.register(User)
class UserAdmin(BaseAdmin):
    add_fieldsets = BaseAdmin.add_fieldsets + (
        ("Personal info", {"fields": (
            "first_name", "last_name", "email")}
         ),
    )
