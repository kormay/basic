from django.db import models
from datetime import datetime

from .Base import Base
from .Role import Role
from .Right import Right

class RoleRight(Base):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    right = models.ForeignKey(Right, on_delete=models.CASCADE)