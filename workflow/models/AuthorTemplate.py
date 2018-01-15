from django.db import models
from workflow.models import ProcessTemplate
from workflow.models import StepTemplate
import uuid


class AuthorTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    process = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE)
    step = models.ForeignKey(StepTemplate, on_delete=models.CASCADE)
    category = models.CharField(max_length=2)
    value = models.CharField(max_length=50)
    name = models.CharField(max_length=50)