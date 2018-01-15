from django.db import models
from .ProcessCategory import ProcessCategory
import uuid


class Process(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    category = models.CharField(null=True, max_length=4)
    form_source = models.CharField(max_length=200)
    data_source = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
