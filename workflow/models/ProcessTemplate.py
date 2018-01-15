from django.db import models
from .ProcessCategory import ProcessCategory
import uuid


class ProcessTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    category = models.CharField(null=True, max_length=4)
    form_source = models.CharField(max_length=200)
    data_source = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1)
