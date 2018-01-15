from django.db import models
import uuid

from secu.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, primary_key=True, editable=False)    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    entry_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name