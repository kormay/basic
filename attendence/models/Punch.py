from django.db import models
from datetime import datetime

from secu.models import User
from .Base import Base

class Punch(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    punch_date = models.DateTimeField(default=datetime.now)
    is_normal = models.BooleanField(default=True)
    IP = models.GenericIPAddressField(max_length=30)