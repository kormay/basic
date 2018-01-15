from django.db import models
from secu.models import User, Base
import uuid

class Status(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    order = models.IntegerField()

class Step(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    order = models.IntegerField()

class Item(Base):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=8000)
    minutes = models.IntegerField(null=True)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    person_in_charge = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def valid(self):
        return True

class ItemWork(Base):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    work = models.CharField(max_length=8000)
    minutes = models.IntegerField()
