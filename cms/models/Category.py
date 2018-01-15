from django.db import models
from .Base import Base


class Category(Base):
    code = models.CharField(primary_key=True,max_length=100)
    title = models.CharField(max_length = 255)