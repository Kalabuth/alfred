from django.contrib import admin

from apps.addresses.models.address import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "street", "latitude", "longitude")
    search_fields = ("street",)
