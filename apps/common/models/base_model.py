import uuid

from django.db.models import BooleanField, DateTimeField, Model, UUIDField


class BaseModel(Model):
    id = UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_staff = BooleanField(default=False)

    class Meta:
        abstract = True

    def disable(self):
        self.is_active = False
        self.save()
