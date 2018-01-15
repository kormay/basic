from django.db import models
from workflow.models import Step
from workflow.models import Author
import uuid


class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1)
