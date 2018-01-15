from django.db import models
from workflow.models import Process
from workflow.models import Step
from workflow.models import Condition


class Relation(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    from_step = models.ForeignKey(Step, related_name='from_step', on_delete=models.CASCADE)
    to_step = models.ForeignKey(Step, related_name='to_step', on_delete=models.CASCADE)
    condition = models.UUIDField(null=True)
