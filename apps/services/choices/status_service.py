from django.db.models import TextChoices


class ServiceStatus(TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
