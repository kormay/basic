from django.db import models
import uuid


class ProcessCategory(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    parent_code = models.CharField(max_length=20, null=True)
    level = models.IntegerField(default=1)
