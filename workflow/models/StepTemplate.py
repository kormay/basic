from django.db import models
from workflow.models import ProcessTemplate
import uuid


class StepTemplate(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    process = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE)
    coordinate_x = models.CharField(null=True,max_length=10)
    coordinate_y = models.CharField(null=True,max_length=10)
