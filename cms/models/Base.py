from django.db import models
from datetime import datetime
from secu.models import User


class Base(models.Model):
    entry_date = models.DateTimeField(auto_now=True) 
    entry_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s", null=True)
    
    class Meta:
        abstract = True