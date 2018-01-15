from django.db import models
from workflow.models import ProcessTemplate
from workflow.models import StepTemplate
from workflow.models import ConditionTemplate


class RelationTemplate(models.Model):
    process = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE)
    from_step = models.ForeignKey(StepTemplate, related_name='from_step', on_delete=models.CASCADE)
    to_step = models.ForeignKey(StepTemplate, related_name='to_step', on_delete=models.CASCADE)
    condition = models.UUIDField(null=True)
