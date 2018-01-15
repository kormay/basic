from django.db import models
from datetime import datetime
from .Employee import Employee
from .Base import Base
from .Adjustment import Adjustment

class AdjustmentLog(Base):
    ADJUSTMENT_OPERATIONS = (
        ('1', 'Approved'),
        ('2', 'Denied'),
    )

    adjustment = models.ForeignKey(Adjustment, on_delete=models.CASCADE)
    operation = models.CharField(max_length=10, choices=ADJUSTMENT_OPERATIONS)