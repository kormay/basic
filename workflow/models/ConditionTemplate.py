from django.db import models
import uuid


class ConditionTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
