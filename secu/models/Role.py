import uuid

from django.db import models
from datetime import datetime

from .Base import Base
from .Right import Right
from .User import User


class Role(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    detail = models.CharField(max_length=8000)
    rights = models.ManyToManyField(Right, through='RoleRight', through_fields=('role', 'right'))
    users = models.ManyToManyField(User, through='UserRole', through_fields=('role', 'user'))
