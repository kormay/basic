from django.db import models
from .Base import Base
from .Category import Category


class Content(Base):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)