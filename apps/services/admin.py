from django.contrib import admin

from apps.services.models.service import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_address",
        "driver",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("id",)
    readonly_fields = ("created_at", "updated_at")
