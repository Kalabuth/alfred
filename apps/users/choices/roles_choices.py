from django.db.models import TextChoices


class RoleChoices(TextChoices):
    CUSTOMER = "customer", "Customer"
    DRIVER = "driver", "Driver"
