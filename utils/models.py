from uuid import uuid4
from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUID(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)

    class Meta:
        abstract = True