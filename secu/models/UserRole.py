from datetime import datetime
from django.db import models

from .Base import Base
from .Role import Role
from .User import User

class UserRole(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    