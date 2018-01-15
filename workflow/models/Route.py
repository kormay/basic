from django.db import models
from workflow.models import Process
from workflow.models import Step


class Route(models.Model):
    id = models.AutoField(primary_key=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    current_step = models.ForeignKey(Step, on_delete=models.CASCADE)
    detail = models.CharField(max_length=1000)
    