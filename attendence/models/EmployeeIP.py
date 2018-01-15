from django.db import models
from datetime import datetime
from secu.models import User
from .Base import Base


class EmployeeIP(Base):
    IP = models.GenericIPAddressField(protocol='IPv4', unpack_ipv4=False, max_length=30, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.IP
