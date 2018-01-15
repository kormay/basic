from django.db import models
from datetime import datetime
from secu.models import User
from .Base import Base

class Adjustment(Base):
    ADJUSTMENT_TYPES = (
        ('L', 'Leave'),
        ('O', 'Over Time'),
    )    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()