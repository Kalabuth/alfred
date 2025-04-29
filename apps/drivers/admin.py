from django.contrib import admin

from apps.drivers.models.driver import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone_number",
        "current_location",
        "is_available",
        "created_at",
    )
    list_filter = ("is_available",)
    readonly_fields = ("created_at", "updated_at")
