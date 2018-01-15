from django.db import models
from workflow.models import Step
import uuid


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    category = models.CharField(max_length=2)
    value = models.CharField(max_length=50)
