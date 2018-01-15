from django.db import models
import uuid


class Condition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
