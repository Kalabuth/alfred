from django.contrib import admin

from apps.customers.models.customer import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "current_location", "phone_number", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("created_at",)
    ordering = ("created_at",)


admin.site.register(Customer, CustomerAdmin)
