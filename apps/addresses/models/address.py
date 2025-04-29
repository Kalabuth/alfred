from django.db.models import CharField, FloatField

from apps.common.models.base_model import BaseModel


class Address(BaseModel):
    street = CharField(max_length=255)
    latitude = FloatField()
    longitude = FloatField()

    def __str__(self):
        return self.street
